terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.23.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

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
          image = "ghcr.io/dilanoch2002/sistema-sensores/sensor-app:latest"
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
}

resource "kubernetes_service" "sensors_service" {
  metadata {
    name = "sensors-service"
  }
  spec {
    selector = {
      app = kubernetes_deployment.sensors_app.spec.0.template.0.metadata.0.labels.app
    }
    port {
      port        = 80
      target_port = 8000
    }
    type = "LoadBalancer"
  }
}