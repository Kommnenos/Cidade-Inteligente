# Diario

## 05-10-2025 – Fase 1

* **Objetivo**: Pipeline mínima funcionando: sensor simulado → IoT Agent → Orion.
  * **Progresso**:
    * Criado `docker-compose.yml` com os componentes mínimos para o ambiente
    * Fluxo de dados básico funcional
      1. Dispositivo é registrado
      2. É postado
      3. Pode ser lido
      4. Recebe registros adicionais
    * simuladores de dados basicos implementados
* **Problemas**:
    * O orion é meio complicadinho na hora de aceitar os parâmetros, também possívelmente deve-se ter cuidado com versões novas quebrando coisas.
    * Acertar as curvas é chato.
* **Próximos Passos**:
    Persistência
    
* **Coisas pra depois**:
    Usar dados do trafego ao invés de inventar
---

## 06-10-2025 – Fase 2
* **Objetivo**: Pipeline mínima funcionando: sensor simulado → IoT Agent → Orion.
    * **Progresso**:
      * Ar usa dados do tráfego
      * Tudo funciona com um comando docker
      * Simuladores produzem dados
    * **Problemas**:
      * Healthchecks causando alguns tropeços.
    * **Próximos Passos**:
      * Persistência
      * Visualizações