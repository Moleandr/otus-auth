

Установка traefik
```shell
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik --values values.yml
```

Запустить приложение
```shell
kubectl apply --recursive -f .k8s
```




