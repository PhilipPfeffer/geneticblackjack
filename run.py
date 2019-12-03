import model as geneticModel
import blackjackGenetic
NUMGENERATIONS = 1000
PLAYERSPERGEN = 300
DECKNUM = 100

def main():
    for threshhold in range(17,22):
        # print(f'---------\nGeneration {0}')
        genModel = geneticModel.GeneticModel()
        genModel.initializeGeneration(PLAYERSPERGEN)
        blackjackGenetic.casino(DECKNUM, genModel.players)
        print(f"random score: {genModel.getAvgScore()}")
        # print(genModel.getAvgScore())


        for i in range(1, NUMGENERATIONS):
            # print(f'---------\nGeneration {i}')
            genModel.select(threshhold)
            genModel.crossover(PLAYERSPERGEN)
            genModel.mutate()
            blackjackGenetic.casino(DECKNUM, genModel.players)
            # print(genModel.getAvgScore())

        # print(genModel)
        print(f"threshhold: {threshhold} --> score: {genModel.getAvgScore()}")

if __name__ == "__main__":
    main()