# Desafio: Enviar email via SMTP

## Descrição

Neste desafio, você irá criar um servidor de email simples que envia emails via SMTP. 
Uma ferramenta que auxilia muito para testar envio de e-mail localmente é o Mailhog: https://github.com/mailhog/MailHog

Seu objetivo é subir uma instância do Mailhog (via docker-compose) e alterar a dependência de `NotificationService` de `Console` para `Email`. Ou seja, o e-mail deve aparecer no Mailhog.
