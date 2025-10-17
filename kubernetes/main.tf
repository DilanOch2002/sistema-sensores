terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.23.0"
    }
  }
}

# CONFIGURACIÓN CORRECTA DEL PROVIDER
provider "kubernetes" {
  config_path = "C:/Users/dilan/.kube/config"  # Ruta ABSOLUTA
}

# SERVICIO B - Sensores (YA EXISTÍA)
resource "kubernetes_deployment" "sensors_app" {
  metadata {
    name = "sensors-app"
    labels = {
      app = "sensors"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "sensors"
      }
    }

    template {
      metadata {
        labels = {
          app = "sensors"
        }
      }

      spec {
        container {
         image = "doch2002/sensor-app:latest"  
          name  = "sensors"

          env {
            name  = "SUPABASE_URL"
            value = "https://vqezennldyqazxjmyrfj.supabase.co"
          }

          env {
            name  = "SUPABASE_KEY"
            value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s"
          }
        }
      }
    }
  }
  wait_for_rollout = false  # ← AGREGAR AL FINAL
}

resource "kubernetes_service" "sensors_service" {
  metadata {
    name = "sensors-service"
  }
  spec {
    selector = {
      app = "sensors"
    }
    port {
      port        = 80
      target_port = 8000
    }
    type = "ClusterIP"
  }
}

# SERVICIO A - Autenticación
resource "kubernetes_deployment" "auth_app" {
  metadata {
    name = "auth-app"
    labels = {
      app = "auth"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "auth"
      }
    }

    template {
      metadata {
        labels = {
          app = "auth"
        }
      }

      spec {
        container {
          name  = "auth"
          image = "doch2002/auth-app:latest"

          env {
            name  = "SUPABASE_URL"
            value = "https://vqezennldyqazxjmyrfj.supabase.co"
          }

          env {
            name  = "SUPABASE_KEY"
            value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s"
          }

          port {
            container_port = 5000
          }
        }
      }
    }
  }
  wait_for_rollout = false  # ← AGREGAR AL FINAL
}

resource "kubernetes_service" "auth_service" {
  metadata {
    name = "auth-service"
  }
  spec {
    selector = {
      app = "auth"
    }
    port {
      port        = 80
      target_port = 5000
    }
    type = "ClusterIP"
  }
}

# SERVICIO C - Ingestión de Datos
resource "kubernetes_deployment" "ingestion_app" {
  metadata {
    name = "ingestion-app"
    labels = {
      app = "ingestion"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "ingestion"
      }
    }

    template {
      metadata {
        labels = {
          app = "ingestion"
        }
      }

      spec {
        container {
          name  = "ingestion"
          image = "doch2002/ingestion-app:latest" 

          env {
            name  = "SUPABASE_URL"
            value = "https://vqezennldyqazxjmyrfj.supabase.co"
          }

          env {
            name  = "SUPABASE_KEY"
            value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s"
          }

          port {
            container_port = 5001
          }
        }
      }
    }
  }
  wait_for_rollout = false  # ← AGREGAR AL FINAL
}

resource "kubernetes_service" "ingestion_service" {
  metadata {
    name = "ingestion-service"
  }
  spec {
    selector = {
      app = "ingestion"
    }
    port {
      port        = 80
      target_port = 5001
    }
    type = "ClusterIP"
  }
}

# SERVICIO D - Gestión de Parcelas
resource "kubernetes_deployment" "plots_app" {
  metadata {
    name = "plots-app"
    labels = {
      app = "plots"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "plots"
      }
    }

    template {
      metadata {
        labels = {
          app = "plots"
        }
      }

      spec {
        container {
          name  = "plots"
          image = "doch2002/plots-app:latest"  

          env {
            name  = "SUPABASE_URL"
            value = "https://vqezennldyqazxjmyrfj.supabase.co"
          }

          env {
            name  = "SUPABASE_KEY"
            value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s"
          }

          port {
            container_port = 5002
          }
        }
      }
    }
  }
  wait_for_rollout = false  # ← AGREGAR AL FINAL
}

resource "kubernetes_service" "plots_service" {
  metadata {
    name = "plots-service"
  }
  spec {
    selector = {
      app = "plots"
    }
    port {
      port        = 80
      target_port = 5002
    }
    type = "ClusterIP"
  }
}
