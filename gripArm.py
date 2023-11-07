import numpy as np
import pygame

FPS = 60  # frames per second

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

colors = [(255, 204, 0), (0, 204, 255), (204, 0, 255), (255, 0, 204), (102, 255, 102), (255, 102, 102), (204, 153, 255),
          (255, 153, 204), (255, 255, 51), (51, 255, 255), (255, 51, 255), (153, 255, 153), (255, 153, 51),
          (102, 102, 255), (255, 102, 255), (153, 255, 255), (255, 51, 153), (255, 51, 51), (153, 51, 255),
          (255, 255, 153), (102, 153, 102), (153, 102, 102), (255, 204, 102), (102, 255, 204), (204, 102, 255),
          (204, 255, 102), (102, 102, 102), (204, 204, 204), (255, 102, 102), (102, 102, 255), (102, 204, 102)]


def Rmat(degree):
    rad = np.deg2rad(degree)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return R


def Tmat(tx, ty):
    Translation = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    return Translation


def getTransformedMatrix(matrix, transMatrix):
    R = transMatrix[:2, :2]
    T = transMatrix[:2, 2]
    Ptransformed = matrix @ R.T + T
    return Ptransformed


class Section:
    def __init__(self, matrix, transformationMatrix, color):
        self.matrix = matrix
        self.transformationMatrix = transformationMatrix
        self.color = color


class Gripper:
    def __init__(self, x, y, w, h, screen):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sectionCount = 0
        self.screen = screen
        self.clawClosed = False
        self.sectionObjects = []
        self.highlightedIndex = 99
        self.matrix = np.array([[0, 0], [self.w, 0], [self.w, self.h], [0, self.h]])

    def createGripper(self, sectionAngles):
        self.createBase()
        for i in range(len(sectionAngles)):
            self.addSection(sectionAngles[i])
        self.createClaw()

    def createBase(self):
        H0 = Tmat(self.x, self.y) @ Tmat(0, -self.h)
        self.sectionObjects.append(Section(getTransformedMatrix(self.matrix, H0), H0, (0, 0, 0)))

    def addSection(self, angle):
        if self.sectionCount == 0:
            self.createFirstSection(angle)
        else:
            self.createNthSection(angle)

    def createFirstSection(self, angle):
        H1 = self.sectionObjects[0].transformationMatrix @ Tmat(self.w / 2, 0)
        H11 = H1 @ Rmat(-90) @ Tmat(0, -self.h / 2)
        H12 = H11 @ Tmat(0, self.h / 2) @ Rmat(angle) @ Tmat(0, -self.h / 2)
        self.sectionObjects.append(Section(getTransformedMatrix(self.matrix, H12), H12, colors[self.sectionCount]))
        self.sectionCount = 1

    def createNthSection(self, angle):
        H2 = self.sectionObjects[self.sectionCount].transformationMatrix @ Tmat(self.w, 0) @ Tmat(0,
                                                                                                  self.h / 2)  # joint 2
        H21 = H2 @ Rmat(angle) @ Tmat(0, -self.h / 2)
        self.sectionObjects.append(Section(getTransformedMatrix(self.matrix, H21), H21, colors[self.sectionCount]))
        self.sectionCount += 1

    def createClaw(self):
        claw = np.array([[0, 0], [60, 0], [60, 10], [0, 10]])
        H2 = self.sectionObjects[self.sectionCount].transformationMatrix @ Tmat(self.w, 0) @ Tmat(0,
                                                                                                  self.h / 2)  # joint 2
        H21 = H2 @ Tmat(0, -self.h / 2)
        H22 = H21 @ Tmat(0, self.h - 10)
        if self.clawClosed:
            H22 = H22 @ Tmat(0, -self.h / 2 + 10)
            H21 = H21 @ Tmat(0, self.h / 2 - 10)

        self.sectionObjects.append(Section(getTransformedMatrix(claw, H21), H21, colors[self.sectionCount]))
        self.sectionObjects.append(Section(getTransformedMatrix(claw, H22), H22, colors[self.sectionCount]))
        self.sectionCount += 2

    def drawSections(self, screen):
        for i in range(len(self.sectionObjects)):
            width = 3
            if i == self.highlightedIndex:
                width = 0

            pygame.draw.polygon(screen, self.sectionObjects[i].color, self.sectionObjects[i].matrix, width)

    def draw(self, sectionAngles, screen):
        self.sectionObjects = []
        self.sectionCount = 0
        self.createGripper(sectionAngles)
        self.drawSections(screen)


def main():
    pygame.init()  # initialize the engine

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    rotateSpeed = 0.5

    # The properties that the arm is based on
    baseW = 100
    baseH = 50
    baseX = (WINDOW_WIDTH / 5) * 4 - baseW / 2
    baseY = (WINDOW_HEIGHT / 20) * 19

    gripper = Gripper(baseX, baseY, baseW, baseH, screen)

    # angles based on which the gripper is made
    angles = [0, 0, 0]

    done = False
    while not done:
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    gripper.clawClosed = not gripper.clawClosed

                else:
                    # get the index from a number input. If the input is not a number the index stays the same
                    gripper.highlightedIndex = numberPressed(event, gripper.highlightedIndex)

        # keep index in bounds
        if gripper.highlightedIndex > gripper.sectionCount - 2:
            gripper.highlightedIndex = gripper.sectionCount - 2

        # ignore the claw
        index = gripper.highlightedIndex - 1

        # Rotate the selected angle based on the rotate speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angles[index] -= rotateSpeed
        if keys[pygame.K_RIGHT]:
            angles[index] += rotateSpeed

        screen.fill((80, 80, 80))
        gripper.draw(angles, screen)
        # finish
        pygame.display.flip()
        clock.tick(FPS)

        # end of while


# end of main()

def numberPressed(event, current):
    index = current
    if event.key == pygame.K_1:
        index = 1
    if event.key == pygame.K_2:
        index = 2
    if event.key == pygame.K_3:
        index = 3
    if event.key == pygame.K_4:
        index = 4
    if event.key == pygame.K_5:
        index = 5
    if event.key == pygame.K_6:
        index = 6
    if event.key == pygame.K_7:
        index = 7
    if event.key == pygame.K_8:
        index = 8
    if event.key == pygame.K_9:
        index = 9
    return index


if __name__ == "__main__":
    main()
