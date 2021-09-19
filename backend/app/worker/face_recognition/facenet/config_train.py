SAMPLING_RATIO=0.4

EPOCHS=10
BATCH_SIZE=20
NEGATIVES_CHOICE=2 # default = 100

IMAGE_SIZE=(224,224)

IMG_PATH="./datasets/after_4_bis/*/*.jpg"
EMBED_IMG_PATH="./datasets/reference_images/*.jpg"
LOG_DIR="logdir_train"

DEVICE="cuda"
MODEL_SAVEPATH="./model_save"