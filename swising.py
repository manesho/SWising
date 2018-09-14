import numpy as np
import random as rnd

# these two functions specify the geometry.
def coord2index(pos, sx, sy):
		return pos[0]%sx * sy + pos[1]%sy;

def index2coord(i, sx, sy):
		return np.array([i//sx, i- (i//sx)*sy])


class World:
		def __init__(self, sx, sy, beta):
			self.ns = sx *sy
			self.sx = sx
			self.sy = sy
			self.padd = 1 - np.exp(-2*beta)
			self.spins=np.full(self.ns, 1, dtype=int)
			self.isdiscovered = np.full((sx*sy), False, dtype=bool)
			deltas = [np.array([0,1]), np.array([0,-1]), np.array([1,0]), np.array([-1,0])]
			self.nblists=[ [coord2index( index2coord(i,sx,sy) + delta, sx, sy)   for delta in deltas]
								for i in range(sx*sy)  ]
		def magnetization(self):
			return self.spins.sum()
		def random(self):
			return rnd.random()
		def swupdate(self):
			# loop over all sites
			for siteindex in range(self.ns):
				# check whether it is already part of a cluster
				if not self.isdiscovered[siteindex]:
					# if not, build a new cluster
					flipthiscluster = True if self.random()<0.5 else False
					# start a queue of spins to process
					queue = [siteindex]
					# mark the spin as part of a cluster
					self.isdiscovered[siteindex]=True
					# process the queue until its empty	
					while len(queue)!=0:
						#take a ssite from the que
						x = queue.pop()
						#enqueue its neighbours with probabilty padd if they are aligned 
						# and 
						for neighbour in self.nblists[x]:
							if not self.isdiscovered[neighbour] and self.spins[x]==self.spins[neighbour]:
								if self.random() < self.padd:
									queue.append(neighbour)
									self.isdiscovered[neighbour] = True
						# Flip the spin at x
						if flipthiscluster: 
							self.spins[x] = self.spins[x] * (-1)
								
		
			# reset the isdiscovered
			self.isdiscovered = np.full( self.ns, False, dtype=bool)
			return 0
		def spinlattice(self):
				return np.array([[self.spins[coord2index((x,y), self.sx,self.sy )] 
										for x in range(self.sx) ]
											for y in range(self.sy)])


def calc_mag(s1, s2, beta):
	return	


