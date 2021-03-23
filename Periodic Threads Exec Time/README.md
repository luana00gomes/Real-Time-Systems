# Compilação
Para compilar, execute no terminal do Linux o seguinte comando na pasta dos arquivos:
g++ teste.cpp -o exe -lrt

Para executar, execute no terminal do Linux o seguinte comando na pasta dos arquivos:
sudo taskset -c 0 ./exe 500 1 9000 R

Em que os argumentos seguem a ordem:
período prioridade fator_de_carga escalonador

Sendo:
R -> SCHED_RR
F -> SCHED_FIFO
