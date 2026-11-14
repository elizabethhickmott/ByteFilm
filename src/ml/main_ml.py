from preproccesor import main_preprocessing
from training import main_training

def main():
    df = main_preprocessing()
    main_training(df)


if __name__ == '__main__':
    main()