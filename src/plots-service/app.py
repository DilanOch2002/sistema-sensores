from flask import Flask, request, jsonify
from supabase import create_client
import os
from datetime import datetime

app = Flask(__name__)

# Configuración Supabase
supabase_url = os.getenv('SUPABASE_URL', 'https://vqezennldyqazxjmyrfj.supabase.co')
supabase_key = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s')
supabase = create_client(supabase_url, supabase_key)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "plots-service running"})

# CRUD de Parcelas
@app.route('/plots', methods=['GET'])
def get_plots():
    try:
        result = supabase.table('plots').select('*').eq('deleted', False).execute()
        return jsonify({
            "plots": result.data,
            "count": len(result.data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plots', methods=['POST'])
def create_plot():
    try:
        plot_data = request.json
        
        # Validaciones básicas
        required_fields = ['name', 'location', 'crop_type', 'responsible']
        for field in required_fields:
            if field not in plot_data:
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Agregar timestamps
        plot_data['created_at'] = datetime.utcnow().isoformat()
        plot_data['updated_at'] = datetime.utcnow().isoformat()
        plot_data['deleted'] = False
        
        # Insertar en Supabase
        result = supabase.table('plots').insert(plot_data).execute()
        
        return jsonify({
            "message": "Parcela creada exitosamente",
            "plot": result.data[0] if result.data else None
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plots/<plot_id>', methods=['GET'])
def get_plot(plot_id):
    try:
        result = supabase.table('plots').select('*').eq('id', plot_id).execute()
        
        if not result.data:
            return jsonify({"error": "Parcela no encontrada"}), 404
            
        return jsonify({"plot": result.data[0]})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plots/<plot_id>', methods=['PUT'])
def update_plot(plot_id):
    try:
        update_data = request.json
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        result = supabase.table('plots').update(update_data).eq('id', plot_id).execute()
        
        if not result.data:
            return jsonify({"error": "Parcela no encontrada"}), 404
            
        return jsonify({
            "message": "Parcela actualizada",
            "plot": result.data[0]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plots/<plot_id>', methods=['DELETE'])
def delete_plot(plot_id):
    try:
        # Obtener datos de la parcela antes de eliminar
plot_result = supabase.table('plots').select('*').eq('id', plot_id).eq('deleted', False).execute()
        
        if not plot_result.data:
            return jsonify({"error": "Parcela no encontrada"}), 404
        
        plot_data = plot_result.data[0]
        
        # Guardar en tabla de eliminados
        deleted_plot = {
            'original_id': plot_data['id'],
            'name': plot_data['name'],
            'location': plot_data['location'],
            'crop_type': plot_data['crop_type'],
            'responsible': plot_data['responsible'],
            'deleted_at': datetime.utcnow().isoformat(),
            'deleted_reason': request.json.get('reason', 'Sin razón especificada')
        }
        
        supabase.table('deleted_plots').insert(deleted_plot).execute()
        
        # Marcar como eliminado en la tabla original (soft delete)
        supabase.table('plots').update({'deleted': True, 'deleted_at': datetime.utcnow().isoformat()}).eq('id', plot_id).execute()
        
        return jsonify({
            "message": "Parcela eliminada y registrada en historial",
            "deleted_plot": deleted_plot
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas adicionales
@app.route('/plots/deleted', methods=['GET'])
def get_deleted_plots():
    try:
        result = supabase.table('deleted_plots').select('*').execute()
        return jsonify({
            "deleted_plots": result.data,
            "count": len(result.data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plots/stats', methods=['GET'])
def get_plots_stats():
    try:
        # Conteo por tipo de cultivo
        crop_stats = supabase.table('plots').select('crop_type', count='exact').eq('deleted', False).execute()
        
        # Total de parcelas
        total_plots = supabase.table('plots').select('*', count='exact').eq('deleted', False).execute()
        
        return jsonify({
            "total_plots": total_plots.count,
            "crop_distribution": crop_stats.data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)