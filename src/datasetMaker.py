from argparse import ArgumentParser
import csv
import os
import random


def makeFakeDataset(filePath):
	with open('doomDataset.csv', 'w', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(["FileName", "CTR"])
		for filename in os.listdir(filePath):
			writer.writerow([os.path.join(filePath, filename), random.uniform(0, 0.6)])

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('--directoryPath', default='N/A')
	args = parser.parse_args()
	makeFakeDataset(args.directoryPath)