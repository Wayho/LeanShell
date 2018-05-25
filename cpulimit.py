# coding: utf-8
import time
import random
import json
#https://docs.python.org/2/library/json.html


###################### Class Define #######################
class Class_Cpu_Dynamic():
	# 等同于Count_Loop_per_Sleep，无输出
	def _Count(self):
		# 总时间已包含sleep总时间（after Start）
		# 给出上次调用Start到本次调用之间每次sleep需要多少次循环的建议
		# 满足throttle，以SLEEP_TIME的sleep为基准

		# 计算本次Count的loop_per_sleep，仅用于输出
		loop_this = self._Get_loop_per_sleep(self.loopnum, self.seconds_cpu)

		# 统计，用于首次Run以来的平均loop_per_sleep
		self._Reduce_SLEEP_TIME()  ## 适应粒度,self.SLEEP_TIME越小越好
		self.total_seconds_cpu += self.seconds_cpu  # 总seconds_cpu时间，秒
		self.total_loopnum += self.loopnum  # 总loopnum的总和
		self.loop_per_sleep = self._Get_loop_per_sleep(self.total_loopnum, self.total_seconds_cpu)
		## loop per sleep ,MUST BE INTERGE
		# 输出
		print( '{:30s} {:6d} | {:6d} loop | {:6.1f}ms | Aver {:8.1f}ms CPU {:8.1f}ms sleep | {}' \
		      .format(self.id, loop_this, self.loop_per_sleep, self.SLEEP_TIME* 1000.0, \
		              self.seconds_cpu/ self.loopnum * 1000.0, self.seconds_sleep/ self.loopnum * 1000.0, self.loopnum, ))

	####################################################
	def Loop_Start(self):
		# 适用于多个实例
		# Loop_Start/Loop_Stop配对使用，不能与Run混用
		# Loop_Start---call fun---Loop_Stop
		self.timestamp = time.time()  # ！！！


	def Loop_Stop(self):
		# 适用于多个实例
		# Loop_Start/Loop_Stop配对使用，不能与Run混用
		# Loop_Start---call fun---Loop_Stop
		self.seconds_cpu += time.time()-self.timestamp
		if (self.loopnum == self.LOOP_MAX):
			# 统计状态触发，统计+复位
			self._Count()
			self.LOOP_MAX *= 2
			self.seconds_cpu = 0.0  # LOOP_MAX统计CPU时间，秒
			self.seconds_sleep = 0.0  # LOOP_MAX统计sleep时间，秒
			self.loopnum = 0L  # loopnum与seconds_sleep,seconds_cpu必须同步置0
		# 默认第一次循环先sleep
		if (0 == self.loopnum % self.loop_per_sleep):
			self.seconds_sleep += self.SLEEP_TIME
			time.sleep(self.SLEEP_TIME)
		# must ++
		self.loopnum += 1L
	####################################################

	# 此函数直接放在循环中，无需Start,Stop
	def Run(self):
		# 适用于只有一个实例
		# 适用于循环极长，且单次耗时较长，需要动态降速的情形，自动统计上次，下次自动配置
		if (self._Run_Has_Called):
			self.seconds_cpu += time.time() - self.timestamp    #上次timestamp为可能的sleep之后，无需减掉sleep
			if (self.loopnum == self.LOOP_MAX):
				# 统计状态触发，统计+复位
				self._Count()
				self.LOOP_MAX *= 2
				self.seconds_cpu = 0.0  # LOOP_MAX统计CPU时间，秒
				self.seconds_sleep = 0.0  # LOOP_MAX统计sleep时间，秒
				self.loopnum = 0L  # loopnum与seconds_sleep,seconds_cpu必须同步置0
		else:
			# 只会执行一次！！！
			self._Run_Has_Called = True
			print('Class_Cpu_Dynamic::Run()\t' + self.id)

		# 默认第一次循环先sleep
		if (0 == self.loopnum % self.loop_per_sleep):
			self.seconds_sleep += self.SLEEP_TIME
			time.sleep(self.SLEEP_TIME)
		# must ++
		self.loopnum += 1L
		self.timestamp = time.time()  # ！！！Run()独有


	def Record_Times(self, strID):
		# 人工调试阶段使用的函数
		# 记录时间戳
		self.timestamp_List.append({"id": strID, "time": time.time()})

	def Record_Output(self, Reset=True):
		# 人工调试阶段使用的函数
		# 统计并输出上次调用到本次调用之间的时间差，ms
		FirstLine = True
		for rec in self.timestamp_List:
			if (FirstLine):
				FirstLine = False
				print(self.id + '.{}\t{:.4f}s\t'.format(rec.get('id'), rec.get('time')))
				time_last = rec.get('time')
			else:
				print(self.id + '.{}\t{:.4f}s\tdelta={:.8f}ms'.format(rec.get('id'), rec.get('time'),
				                                                      (rec.get('time') - time_last) * 1000))
				time_last = rec.get('time')
		if (Reset):
			self.timestamp_List = []
			print("=============================================")
		else:
			print("+++++++++++++++++++++++++++++++++++++++++++++")

	def Reset(self):
		# 复位，除了self.loop_per_sleep+self.SLEEP_TIME
		self.timestamp_List = []
		self._Run_Has_Called = False  # 运行Run()后置True,用于记录最开始的时间TIMESTAMP
		self.LOOP_MAX = 1  # Dynamic,>=1

		self.total_seconds_cpu = 0.0  # 总seconds_cpu时间，秒
		self.total_loopnum = 0L  # 总loopnum的总和

		self.seconds_cpu = 0.0  # LOOP_MAX统计CPU时间，秒
		self.seconds_sleep = 0.0  # LOOP_MAX统计sleep时间，秒, 可以不要！！！
		self.loopnum = 0L  # loopnum与seconds_sleep,seconds_cpu必须同步置0
		print('Class_Cpu_Dynamic::Reset()\t' + self.id)

	############## private ################
	def __init__(self, strID, throttle=0.7):
		self.id = strID
		self.throttle = throttle  # throttle=0.7==30%CPU usage

		self.loop_per_sleep = 1L  # default is 1 loop sleep, reset by Run()，小于50时需要调整SLEEP_TIME
		self.SLEEP_TIME = 0.05  # 50 ms,允许以10ms为单位增加，以适应loop_per_sleep太小带来的粒度不够

		self.Reset()

	def _Get_loop_per_sleep(self, loopnum, seconds_cpu):
		# 计算loop_per_sleep建议
		# loopnum:循环次数
		# seconds_cpu：CPU费时
		# 返回：loop_per_sleep >= 1, long int
		seconds_dest = seconds_cpu / (1.0 - self.throttle)  # 目标总时间=CPUcall time/变比
		seconds_sleep_dest = seconds_dest - seconds_cpu
		loop_per_sleep = long(loopnum * self.SLEEP_TIME / seconds_sleep_dest)
		while (0 == loop_per_sleep):
			self.SLEEP_TIME = 1.05 * self.SLEEP_TIME
			loop_per_sleep = long(loopnum * self.SLEEP_TIME / seconds_sleep_dest)
		return loop_per_sleep

	def _Reduce_SLEEP_TIME(self):
		# int loop_per_sleep
		# 尝试重设self.SLEEP_TIME，越小越好>=0.05
		if (0.065 <= self.SLEEP_TIME):  # 按1.3倍减小self.SLEEP_TIME
			self.SLEEP_TIME = self.SLEEP_TIME / 1.3
		elif (0.055 <= self.SLEEP_TIME):
			self.SLEEP_TIME = self.SLEEP_TIME / 1.1

	'''		
	def _LoadDefault(self):
		self.jsonfile = 'cpulimit.json'  # json file:default loop_per_sleep by id
		filetext = Load_From_File(self.jsonfile)
		JsonAll = json.loads(filetext)
		#print ('{}'.format(JsonAll))
		for aJson in JsonAll:
			if(cmp(aJson.get("ID"),self.id)==0):
				self.loop_per_sleep = aJson.get("LOOP")
				self.SLEEP_TIME = aJson.get("SLEEP")
	'''

CPULIMIT_STATIC = Class_Cpu_Dynamic('STATIC')

def Fun_50ms():
	# Intel(R) Core(TM) i5 CPU 650 @ 3.20GHz # 1560MHz, 10ms=158800L
	# Intel Core Processor (Broadwell) # 2196 MHz
	for i in range(0, 795000L):
		a = 0.038 / 1000.0

def Fun_5ms():
	# Intel(R) Core(TM) i5 CPU 650 @ 3.20GHz # 1560MHz, 10ms=158800L
	# Intel Core Processor (Broadwell) # 2196 MHz
	for i in range(0, 79500L):
		a = 0.038 / 1000.0

def Fun_1ms():
	# Intel(R) Core(TM) i5 CPU 650 @ 3.20GHz # 1560MHz, 10ms=158800L
	# Intel Core Processor (Broadwell) # 2196 MHz
	for i in range(0, 15880L):
		a = 0.038 / 1000.0

def Test_Run(loop):
	for i in range(0,loop):
		Fun_5ms()
		CPULIMIT_STATIC.Run()


def Test():
	for i in range(1,5):
		Test_Run(i*400)

#Test_Loop_Throttle_Auto()
#Test()

#########################################
CPULIMIT_main_train_model = Class_Cpu_Dynamic("main.train.model")
CPULIMIT_main_train_nll_loss = Class_Cpu_Dynamic("main.train.nll_loss")
CPULIMIT_main_train_backward = Class_Cpu_Dynamic("main.train.backward")
