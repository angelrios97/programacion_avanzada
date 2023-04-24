# Ejecuta varias veces las baterías de pruebas tests.py y tests_bnlearn.py.
# Comando: ./run_tests.sh
# Comando: ./run_tests.sh 10

if [ $# -eq 0 ]  # Si no se le pasan argumentos,
then
  niter=5  # ejecuta los tests 5 veces.
else
  niter=$1  # En caso contrario, los ejecuta tantas veces como el argumento.
fi

# Ejecutamos repetidamente tests.py y tests_bnlearn.py
for rep in $(seq 1 $niter)
 do
   echo "Ejecución" $rep "tests.py"
   python3 tests.py
done
for rep in $(seq 1 $niter)
  do
    echo "Ejecución" $rep "tests_bnlearn.py"
    python3 tests_bnlearn.py
done