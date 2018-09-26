from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, UpSampling2D, Reshape, core, Dropout, Cropping2D
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as K
from keras.utils.vis_utils import plot_model
from keras.optimizers import SGD


#Define the neural network
def get_slidenet(n_ch=3,patch_height=818,patch_width=818): #(3,818,818)
    inputs = Input(shape=(n_ch, patch_height, patch_width))

    conv1 = Conv2D(32, (3, 3), activation='relu',data_format='channels_first')(inputs)
    conv1 = Conv2D(32, (3, 3), activation='relu', data_format='channels_first')(conv1)
    conv1 = Conv2D(32, (3, 3), activation='relu', data_format='channels_first')(conv1)
    pool1 = MaxPooling2D((2, 2))(conv1)

    conv2 = Conv2D(64, (3, 3), activation='relu',data_format='channels_first')(pool1)
    conv2 = Conv2D(64, (3, 3), activation='relu', data_format='channels_first')(conv2)
    conv2 = Conv2D(64, (3, 3), activation='relu', data_format='channels_first')(conv2)
    pool2 = MaxPooling2D((2, 2))(conv2)

    conv3 = Conv2D(128, (3, 3), activation='relu', data_format='channels_first')(pool2)
    conv3 = Conv2D(128, (3, 3), activation='relu', data_format='channels_first')(conv3)
    pool3 = MaxPooling2D((2, 2))(conv3)

    conv4 = Conv2D(256, (3, 3), activation='relu', data_format='channels_first')(pool3)
    conv4 = Conv2D(256, (3, 3), activation='relu', data_format='channels_first')(conv4)
    conv4 = Conv2D(256, (3, 3), activation='relu', data_format='channels_first')(conv4)
    pool4 = MaxPooling2D((2, 2))(conv4)

    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same', data_format='channels_first')(pool4)

    up1 = UpSampling2D(size=(2,2))(conv5)
    up1 = concatenate([conv4,up1],axis=1)
    conv6 = Conv2D(768, (3, 3), activation='relu', data_format='channels_first')(up1)
    conv6 = Conv2D(384, (3, 3), activation='relu', data_format='channels_first')(conv6)
    conv6 = Conv2D(192, (3, 3), activation='relu', data_format='channels_first')(conv6)

    up2 = UpSampling2D(size=(2,2))(conv6)
    crop_conv3 = Cropping2D(cropping=((12, 12), (12, 12)))(conv3)
    up2 = concatenate([crop_conv3,up2],axis=1)
    conv7 = Conv2D(320, (3, 3), activation='relu', data_format='channels_first')(up2)
    conv7 = Conv2D(160, (3, 3), activation='relu', data_format='channels_first')(conv7)

    up3 = UpSampling2D(size=(2, 2))(conv7)
    crop_conv2 = Cropping2D(cropping=((32, 32), (32, 32)))(conv2)
    up3 = concatenate([crop_conv2,up3],axis=1)
    conv8 = Conv2D(224, (3, 3), activation='relu', data_format='channels_first')(up3)
    conv8 = Conv2D(112, (3, 3), activation='relu', data_format='channels_first')(conv8)
    conv8 = Conv2D(56, (3, 3), activation='relu', data_format='channels_first')(conv8)

    up4 = UpSampling2D(size=(2, 2))(conv8)
    crop_conv1 = Cropping2D(cropping=((76, 76), (76, 76)))(conv1)
    up4 = concatenate([crop_conv1,up4],axis=1)
    conv9 = Conv2D(88, (3, 3), activation='relu', data_format='channels_first')(up4)
    conv9 = Conv2D(44, (3, 3), activation='relu', data_format='channels_first')(conv9)
    conv9 = Conv2D(22, (3, 3), activation='relu', data_format='channels_first')(conv9)

    conv10 = Conv2D(2, (1, 1), activation='relu', data_format='channels_first')(conv9)
    conv10 = Dropout(0.2)(conv10)
    conv10 = core.Reshape((2, 654 * 654))(conv10)
    conv10 = core.Permute((2, 1))(conv10)
    softmax = core.Activation('softmax')(conv10)
    model = Model(input=inputs, output=softmax)

    # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.3, nesterov=False)
    model.compile(optimizer=SGD(lr=0.001), loss='categorical_crossentropy',metrics=['accuracy'])

    return model