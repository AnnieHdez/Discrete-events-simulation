import random
import math
import numpy as np

#Variables Globales
#Inicializar el tiempo y la cantidad de clientes en 0
t = n = na = 0
#No hay clientes por lo que los tiempos de salida son infinitos
t1 = t2 = t3 = np.inf

#Tiempo en minutos de los horarios picos y de cierre
close_time = 660
begin_rush_hour1 = 90
end_rush_hour1 = 210
begin_rush_hour2 = 420
end_rush_hour2 = 540

#Van a guardar la hora de llegada y atención de cada cliente
arraivals = []
get_service = []

#Va a representar la cola en todo momento, las 3 primeras posiciones van a
#ser los clientes que están siendo atendido por los camareros,-1 si no hay
line = [-1,-1,-1]

def KojoKitchen(new_waiter):
	global t1, t2, t3, t, n, na
	global close_time, begin_rush_hour1, begin_rush_hour2, end_rush_hour1, end_rush_hour2

	#Generar el tiempo de llegada del primer cliente
	ta = exponential(8/60)

	#Si la llegada del primer cliente es después que cierren no se hace nada
	if ta > close_time:
		exit()
	print("Va a llegar el 1er cliente en " + str(ta))
	

	while True:

		ts = [t1, t2, t3]
		ti = min(ta, t1, t2)
		#Si hay clientes esperando y estamos usando un tercer camarero y este está libre y le toca empezar a trabajar
		if n > 2 and new_waiter and t3 == np.inf and ((ti >= begin_rush_hour1 and t <= end_rush_hour1) or (ti >= begin_rush_hour2 and t <= end_rush_hour2)):
			if t <= end_rush_hour1:
				t = begin_rush_hour1
			else:
				t= begin_rush_hour2

			get_service.insert(line[3], t)

			#Hacer que el camarero atienda al 1er cliente en la cola
			num = line[3]
			line.remove(num)
			line[2] = num
			if random.randint(0, 1) == 0:
				t3 = t + np.random.uniform(low=3, high=5)
				print("Atiende 3 al cliente " + str(num) + " y pidió sandwich se va a las " + str(t3))

			else:
				t3 = t + np.random.uniform(low=5, high=8)
				print("Atiende 3 al cliente " + str(num) + " y pidió sushi se va a las " + str(t3))

			print(str(line))
			print("")
			continue

		#El próximo evento es la llegada de un cliente
		if ta <= t1 and ta <= t2 and ta <= t3 and ta <= close_time:
			print("Llegó el cliente " + str(na) + " a las " + str(ta))
			t = ta
			n += 1
			arraivals.insert(na,t)

			#Si alguno de los dos camareros está disponible lo atienden
			if line[0] == -1:
				get_service.insert(na, t)
				line[0] = na 
				if random.randint(0, 1) == 0:
					t1 = t + np.random.uniform(low=3, high=5)
					print("Lo atiende 1 y pidió sandwich se va a las " + str(t1))

				else:
					t1 = t + np.random.uniform(low=5, high=8)
					print("Lo atiende 1 y pidió sushi se va a las " + str(t1))

			elif line[1] == -1:
				get_service.insert(na, t)
				line[1] = na
				if random.randint(0, 1) == 0:
					t2 = t + np.random.uniform(low=3, high=5)
					print("Lo atiende 2 y pidió sandwich, se va a las " + str(t2))

				else:
					t2 = t + np.random.uniform(low=5, high=8)
					print("Lo atiende 2 y pidió sushi, se va a las " + str(t2))

			#Si estamos usando al 3er camarero y es una hora en la que trabaja y está disponible entonces atiende al cliente
			elif new_waiter and ((ta >= begin_rush_hour1 and ta <= end_rush_hour1) or (ta >= begin_rush_hour2 and ta <= end_rush_hour2)) and line[2] == -1:
					get_service.insert(na, t)
					line[2] = na
					if random.randint(0, 1) == 0:
						t3 = t + np.random.uniform(low=3, high=5)
						print("Lo atiende 3 y pidió sandwich, se va a las " + str(t3))

					else:
						t3 = t + np.random.uniform(low=5, high=8)
						print("Lo atiende 3 y pidió sushi, se va a las " + str(t3))

			#Si no puede atenderlo ningún camarero se pone al final de la cola
			else:
				line.append(na)

			#Si estamos en horario pico van a llegar más segido los clientes
			if(t >= begin_rush_hour1 and t <= end_rush_hour1) or (t >= begin_rush_hour2 and t <= end_rush_hour2):
				#Generamos el tiempo de llegada del próximo cliente
				ta = t + exponential(16/60)

			else:
				ta = t + exponential(8/60)

			#No puede llegar después que cierren, así que no va a ocurrir
			if ta > close_time:
				ta = np.inf
			else:
				print("Va a llegar el próximo cliente a las " + str(ta))
				
			na += 1
			print(str(line))
			print("")
			continue

		#El próximo evento es la salida del cliente atendido por el camerero 1 
		if t1 < ta and t1 <= t2 and t1 <= t3:
			if serve_waiter (0, ts, ta):
				break
			t1 = ts[0]
			t2 = ts[1]
			t3 = ts[2]
			continue

		#El próximo evento es la salida del cliente atendido por el camerero 2
		if t2 < ta and t2 < t1 and t2 <= t3:
			if serve_waiter (1, ts, ta):
				break
			t1 = ts[0]
			t2 = ts[1]
			t3 = ts[2]
			continue

		#El próximo evento es la salida del cliente atendido por el camerero 3
		if t3 < ta and t3 < t1 and t3 < t2:
			if serve_waiter (2, ts, ta):
				break
			t1 = ts[0]
			t2 = ts[1]
			t3 = ts[2]
			continue

	count = 0
	for i in range(0, len(arraivals)):
		if get_service[i] - arraivals[i] > 5:
			count += 1

	print("Esperaron más de 5 min el "+str(count *100 / na) + "% de los clientes " + str(na) + " "+ str(count))


#El camerero número waiter_index acaba de atender a un cliente
def serve_waiter (waiter_index, ts, ta):
	global t, n, begin_rush_hour1, begin_rush_hour2, end_rush_hour1, end_rush_hour2

	print("Se fue el cliente " + str(line[waiter_index]) + " a las " + str(ts[waiter_index]))
	
	t = ts[waiter_index]
	n -= 1

	#Si no hay más ningún cliente por atender y no va a llegar más ninguno terminar
	if n == 0 and ta == np.inf:
		return True 

	#Si no hay más ningún cliente por atender, o es el camarero 3 y está fuera de su horario, poner al camarero como libre y no va a salir más ningún cliente
	elif (waiter_index != 2 and (n < 2 or (n < 3 and ts[2] < np.inf))) or ( waiter_index == 2 and (n < 3 or (t < begin_rush_hour1 or t > end_rush_hour2 or (t > end_rush_hour1 and t < begin_rush_hour2)))):
		ts[waiter_index] = np.inf
		line[waiter_index] = -1

	#Hacer que el camarero atienda al próximo cliente en la cola
	else:
		num = line[3]
		line.remove(num)
		line[waiter_index] = num
		get_service.insert(num, ts[waiter_index])
		if random.randint(0, 1) == 0:
			ts[waiter_index] = t + np.random.uniform(low=3, high=5)
			print("Atiende " + str(waiter_index + 1) +" al cliente " + str(num) + " y pidió sandwich se va a las " + str(ts[waiter_index]))

		else:
			ts[waiter_index] = t + np.random.uniform(low=5, high=8)
			print("Atiende " + str(waiter_index + 1) +" al cliente " + str(num) + " y pidió sushi se va a las " + str(ts[waiter_index]))

	print(str(line))
	print("")
	return False

def exponential(lambd):
	random = np.random.uniform()
	return -(math.log(1- random))/lambd


KojoKitchen(True)