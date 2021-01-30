#Create by Quan-11, 2020/07/19
#tower_blaster

def shuffle(bricks):
	# 洗牌功能，将列表中的元素随机打乱顺序
	import random
	random.shuffle(bricks)


def check_bricks(main_pile, discard):
	''' 检查给定的主砖块堆中是否还有剩余的牌。
		如果没有，将弃堆重新洗牌后，移到主砖块堆上。
		然后把主砖块堆最上面的一张牌翻过来作为新弃牌堆的第一块砖。
	'''
	if (len(main_pile) == 0):
		shuffle(discard)
		main_pile.extend(discard)
		#main_pile = discard[:]
		discard = []
		main_pile_popped = main_pile.pop(0)
		discard.insert(0, main_pile_popped)


def check_tower_blaster(tower):
	# 判断塔堆中的砖块顺序是否达到了稳定状态，即按照从小到大的顺序排列
	import operator
	sorted_tower = sorted(tower)
	if (operator.eq(sorted_tower, tower) == 1):
		return True
	else:
		return False


def get_top_brick(brick_pile):
	'''取出堆中的最上面的砖块
		此函数用于在游戏开始时，取主堆最上面的砖块放到弃堆中。
		它也在每个玩家的回合中使用，从弃堆或主堆中取出最上面的砖块。
	'''
	top_brick = brick_pile.pop(0)
	return int(top_brick)


def deal_initial_bricks(main_pile):
	'''开始游戏时，电脑和玩家的塔各有十个砖块。
		此函数返回两个列表，一个表示玩家的塔堆，另一个表示电脑的塔堆。 
		砖块首先给电脑，然后按照一块交给电脑，一块给玩家，一块给电脑，一块给玩家的顺序发放砖块，依此类推。
	'''
	shuffle(main_pile)
	computer_pile = []
	player_pile = []
	for i in range(0,10):
		computer_pile.insert(0, get_top_brick(main_pile)) 
		player_pile.insert(0, get_top_brick(main_pile)) 
	return (computer_pile, player_pile)


def add_brick_to_discard(brick, discard):
	# 将砖块添加到弃堆的顶部
	discard.insert(0 , brick)


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard): 
	'''在塔中找到需要更换的砖块，并用新砖块替换。
		检查并确保要更换的砖确实是塔中的砖。
		然后将要更换的砖放在弃堆的顶部。
		函数的返回值，如果进行了砖块的更换，返回True，没有进行砖块的更换，则返回False
	'''
	if (brick_to_be_replaced in tower):
		p = tower.index(brick_to_be_replaced)
		tower[p] = new_brick
		add_brick_to_discard(brick_to_be_replaced , discard)
		return True
	else:
		return False


def computer_play(tower, main_pile, discard):
	# 电脑的决策
	brick = get_top_brick(main_pile)
	# 设定电脑总是选择主堆中的砖块，并总是使用它进行砖块替换
	if brick in range(1,31):
		# 如果给定砖块在1-30之间，那么只与塔中前半部分（1-5）的砖块交换
		if (brick in range(1,16)):
			# 如果给定砖块在1-15之间，则第1个到第5个依次比较，如果塔中砖块大于给定砖块，则替换。
			for i in range(0,5):
				if tower[i] > brick:
					find_and_replace(brick, tower[i], tower, discard)
					break
		else:
			for i in range(4,-1,-1):
				# 如果给定砖块在16-30之间，则第5个到第1个依次比较，如果塔中砖块小于给定砖块，则替换。
				if tower[i] < brick:
					find_and_replace(brick, tower[i], tower, discard)
					break

	else:
		# 如果给定砖块在31-60之间，那么只与塔中后半部分（6-10）的砖块交换
		if brick in range(31,46):
			# 如果给定砖块在31-45之间，则第6个到第10个依次比较，如果塔中砖块大于给定砖块，则替换。
			for i in range(5,10):
				if tower[i] > brick:
					find_and_replace(brick, tower[i], tower, discard)
					break
		else:
			# 如果给定砖块在46-60之间，则第10个到第6个依次比较，如果塔中砖块小于给定砖块，则替换。
			for i in range(9,4,-1):
				if tower[i] < brick:
					find_and_replace(brick, tower[i], tower, discard)
					break
	return tower


def main():
	main_pile = list(range(1,61))
	discard = []
	computer_tower = []
	player_tower = []
	computer_tower , player_tower= deal_initial_bricks(main_pile)
	discard.append(get_top_brick(main_pile))

	print("\tGame Begin!\nTip:You will play as player\n")
	print("\tcomputer tower:" + str(computer_tower) + "\n")
	print("\tplayer tower:" + str(player_tower) + "\n")

	# 游戏开始
	while True:
		check_bricks(main_pile, discard)
		computer_tower = computer_play(computer_tower, main_pile, discard)
		# 电脑先进行操作
		if(check_tower_blaster(computer_tower) == True):
			print("\n\tcomputer tower:" + str(computer_tower) + "\n")
			print("You Lost.")
			break
			# 检测电脑的塔是否按照从小到大的顺序，若是，则电脑获胜，玩家失败
		else:
		# 玩家进行操作
			check_bricks(main_pile, discard)
			print("The top brick in discard is " + str(discard[0]) + "\n")
			print("Do you want to see the top brick of the main pile? \n")
			key1 = input("Please input Y or N ———— ")
			while key1 != "Y" and key1 !="y" and key1 != "N" and key1 != "n":
				key1 = input("\nPlease enter a valid choice [Y/N] ")

			if ((key1 == "Y") or (key1 == "y")):
			# 玩家选择查看主堆砖块
				top_main_brick = get_top_brick(main_pile)
				print("\nThe top brick in main pile is " + str(top_main_brick) + "\n")
				print("Do you want to use this brick? \n")
				key2 = input("Please input Y or N ———— ")
				while key2 != "Y" and key2 !="y" and key2 != "N" and key2 != "n":
					key2 = input("\nPlease enter a valid choice [Y/N] ")

				if ((key2 == "Y") or (key2 == "y")):
				# 玩家选择使用主堆砖块
					to_replace = input("\nPlease input the brick you want to replace in your tower.———— ")
					# 玩家输入塔中要被替换的砖块
					while (to_replace.isdigit() == False):
					# 玩家输入不是数字，提示错误
						to_replace = input("\nPlease input the brick you want to replace in your tower.And make sure the input is a number between 1 and 60———— ")
					to_replace = int(to_replace)

					while not (find_and_replace(top_main_brick, to_replace, player_tower, discard)):
					# 玩家数入数字在玩家的塔中没有找到，提示错误
						to_replace = int(input("\nCan not find this brick in your tower, please try another input.———— "))
					print("\n\tplayer tower:" + str(player_tower) + "\n")
					if (check_tower_blaster(player_tower) == True):
					# 检测进行砖块替换后，玩家是否获胜
						print("You Win!")
						break
				elif ((key2 == "N") or (key2 == "n")):
					add_brick_to_discard(top_main_brick, discard)
					# 玩家查看主堆砖块后，选择不使用

			elif ((key1 == "N") or (key1 == "n")):
			# 玩家选择不查看主堆砖块，直接使用弃堆砖块
				to_replace = input("\nPlease input the brick you want to replace in your tower.———— ")
				# 玩家输入塔中要被替换的砖块
				while (to_replace.isdigit() == False):
				# 玩家输入不是数字，提示错误
					to_replace = input("\nPlease input the brick you want to replace in your tower.And make sure the input is a number between 1 and 60———— ")
				to_replace = int(to_replace)

				while not (find_and_replace(discard[0], to_replace, player_tower, discard)):
				# 玩家数入数字在玩家的塔中没有找到，提示错误
					to_replace = int(input("\nCan not find this brick in your tower, please try another input.———— "))

				print("\n\tplayer tower:" + str(player_tower) + "\n")
				if (check_tower_blaster(player_tower) == True):
				# 检测进行砖块替换后，玩家是否获胜
					print("You Win!")
					break
				


if __name__ == '__main__':
	main()



