# Desafio: Cancel Subscription API

Neste desafio, você deve implementar a API de cancelamento de assinaturas seguindo o padrão utilizado nas demais APIs do
projeto.

## Requisitos

1. Seguir o contrato da API:
```
DELETE /subscriptions/{subscription_id}/
```

2. Implementar testes end-to-end para o cancelamento de assinaturas para os casos:
   - Cancelar assinatura ativa: Response: 200 OK
   - Cancelar assinatura inexistente: Response: 404 NOT_FOUND
