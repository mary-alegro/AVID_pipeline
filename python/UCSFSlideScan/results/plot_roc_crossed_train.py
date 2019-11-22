import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc



def main():

    #AT100 segmented using model trained with AT8
    test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT100/results/testing/AT100_testing_stats.npy')
    val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT100/results/validation/AT100_validation_stats.npy')
    cross_test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT100/results_trained_with_AT8/testing/AT100_AT8_testing_stats.npy')
    cross_val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT100/results_trained_with_AT8/validation/AT100_AT8_validation_stats.npy')
    fig1_name = '/home/maryana/storage2/Posdoc/AVID/AT100/results/validation/AT100_trained_with_AT8_ROC.png'

    auc_test = auc(test_stats[:, 5], test_stats[:, 3])
    auc_val = auc(val_stats[:, 5], val_stats[:, 3])
    cross_auc_test = auc(cross_test_stats[:, 5], cross_test_stats[:, 3])
    cross_auc_val = auc(cross_val_stats[:, 5], cross_val_stats[:, 3])

    plt.figure()
    lw = 2
    plt.plot(test_stats[:, 5], test_stats[:, 3], color='darkorange',lw=lw, label='Testing (AUC {:.4f})'.format(auc_test))
    plt.plot(val_stats[:, 5], val_stats[:, 3], color='purple', lw=lw, label='Validation (AUC {:.4f})'.format(auc_val))
    plt.plot(cross_test_stats[:, 5], cross_test_stats[:, 3], color='red',lw=lw, label='Testing AT100/AT8 (AUC {:.4f})'.format(cross_auc_test))
    plt.plot(cross_val_stats[:, 5], cross_val_stats[:, 3], color='blue', lw=lw, label='Validation AT100/AT8 (AUC {:.4f})'.format(cross_auc_val))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()

    plt.savefig(fig1_name)


    #AT8 segmented using model trained with AT100
    test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT8/results/testing/AT8_testing_stats.npy')
    val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT8/results/validation/AT8_validation_stats.npy')
    fig2_name = '/home/maryana/storage2/Posdoc/AVID/AT8/results/validation/AT8_ROC.png'

    auc_test = auc(test_stats[:, 5], test_stats[:, 3])
    auc_val = auc(val_stats[:, 5], val_stats[:, 3])

    plt.figure()
    lw = 2
    plt.plot(test_stats[:, 5], test_stats[:, 3], color='darkorange',lw=lw, label='Testing ROC (AUC {:.2f})'.format(auc_test))
    plt.plot(val_stats[:, 5], val_stats[:, 3], color='purple', lw=lw, label='Validation ROC (AUC {:.2f})'.format(auc_val))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('AT8 Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()

    #plt.savefig(fig2_name)

    #MC1 segmented using model trained with AT100
    test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/MC1/results/testing/MC1_testing_stats.npy')
    val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/MC1/results/validation/MC1_validation_stats.npy')
    fig2_name = '/home/maryana/storage2/Posdoc/AVID/MC1/results/validation/MC1_ROC.png'

    auc_test = auc(test_stats[:, 5], test_stats[:, 3])
    auc_val = auc(val_stats[:, 5], val_stats[:, 3])

    plt.figure()
    lw = 2
    plt.plot(test_stats[:, 5], test_stats[:, 3], color='darkorange',lw=lw, label='Testing ROC (AUC {:.2f})'.format(auc_test))
    plt.plot(val_stats[:, 5], val_stats[:, 3], color='purple', lw=lw, label='Validation ROC (AUC {:.2f})'.format(auc_val))
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('MC1 Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()

    plt.savefig(fig2_name)

    pass


if __name__ == '__main__':
    main()