# Desafio: Renew Subscription API

Neste desafio, você deve implementar a API de renovação de assinaturas seguindo o padrão utilizado nas demais APIs do
projeto.

## Requisitos

1. Seguir o contrato da API:
```
POST /subscriptions/{subscription_id}/renew/

Request Body:
{
  "subscription_id": "75cdee06-d4d8-4362-9686-68cd60e36acc",
  "payment_token": "my-payment-token",
}

Response: 200 OK
```


> Lembre-se de como podemos sobrescrever a dependênciad o PaymentGateway para simular o sucesso ou falha do pagamento.
```python
app.dependency_overrides[get_payment_gateway] = lambda: FakePaymentGateway(success=False)
```


2. Casos de teste end-to-end para a renovação de assinaturas:
   - Renovar assinatura REGULAR -> Estender assinatura: HTTP 200
   - Renovar assinatura REGULAR e pagamento FALHAR -> Converter para TRIAL: HTTP 200
   - Renovar assinatura TRIAL -> upgrade para regular: HTTP 200
   - Renovar assinatura TRIAL e pagamento FALHAR -> Cancelar assinatura: HTTP 200
   - Renovar assinatura inexistente: Response: 404 NOT_FOUND
