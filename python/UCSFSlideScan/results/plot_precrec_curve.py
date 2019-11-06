import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc

def find_nearest1(array,value):
    idx,val = min(enumerate(array), key=lambda x: abs(x[1]-value))
    return idx


def main():

    thres = 0.7


    #AT100
    test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT100/results/testing/AT100_testing_stats.npy')
    val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT100/results/validation/AT100_validation_stats.npy')
    fig1_name = '/home/maryana/storage2/Posdoc/AVID/AT100/results/validation/AT100_precision_recall.png'

    prec_t = test_stats[:, 2]
    recall_t = test_stats[:, 3]
    prec_v = val_stats[:, 2]
    recall_v = val_stats[:, 3]

    probs = np.linspace(1, 0, num=20)
    index = find_nearest1(probs,thres)

    x_thres_t = recall_t[index]
    y_thres_t = prec_t[index]
    x_thres_v = recall_v[index]
    y_thres_v = prec_v[index]

    plt.figure()
    lw = 2
    plt.plot(recall_t,prec_t, color='darkorange',lw=lw, label='Testing')
    plt.plot(recall_v,prec_v,  color='purple', lw=lw, label='Validation')
    plt.plot(x_thres_t, y_thres_t, color='red', lw=lw, marker='*', markersize=12) # Testing threshold tirado dos vetores prec/recall usando o index de probs mais proximos do threshold = 0.7
    plt.plot(x_thres_v, y_thres_v, color='red', lw=lw, marker='*', markersize=12)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('AT100 Precision-Recall Curve')
    plt.legend(loc="lower right")
    plt.show()

    plt.savefig(fig1_name)


    # #AT8
    # test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT8/results/testing/AT8_testing_stats.npy')
    # val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/AT8/results/validation/AT8_validation_stats.npy')
    # fig2_name = '/home/maryana/storage2/Posdoc/AVID/AT8/results/validation/AT8_precision_recall.png'
    #
    # prec_t = test_stats[:, 2]
    # recall_t = test_stats[:, 3]
    # prec_v = val_stats[:, 2]
    # recall_v = val_stats[:, 3]
    #
    # probs = np.linspace(1, 0, num=20)
    # index = find_nearest1(probs,thres)
    #
    # x_thres_t = recall_t[index]
    # y_thres_t = prec_t[index]
    # x_thres_v = recall_v[index]
    # y_thres_v = prec_v[index]
    #
    # plt.figure()
    # lw = 2
    # plt.plot(recall_t,prec_t, color='darkorange',lw=lw, label='Testing')
    # plt.plot(recall_v,prec_v,  color='purple', lw=lw, label='Validation')
    # plt.plot(x_thres_t, y_thres_t, color='red', lw=lw, marker='*', markersize=12) # Testing threshold tirado dos vetores prec/recall usando o index de probs mais proximos do threshold = 0.7
    # plt.plot(x_thres_v, y_thres_v, color='red', lw=lw, marker='*', markersize=12)
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    # plt.xlabel('Recall')
    # plt.ylabel('Precision')
    # plt.title('AT8 Precision-Recall Curve')
    # plt.legend(loc="lower right")
    # plt.show()
    #
    #
    # plt.savefig(fig2_name)

    # MC1
    test_stats = np.load('/home/maryana/storage2/Posdoc/AVID/MC1/results/testing/MC1_testing_stats.npy')
    val_stats = np.load('/home/maryana/storage2/Posdoc/AVID/MC1/results/validation/MC1_validation_stats.npy')
    fig2_name = '/home/maryana/storage2/Posdoc/AVID/MC1/results/validation/MC1_precision_recall.png'

    prec_t = test_stats[:, 2]
    recall_t = test_stats[:, 3]
    prec_v = val_stats[:, 2]
    recall_v = val_stats[:, 3]

    probs = np.linspace(1, 0, num=20)
    index = find_nearest1(probs, thres)

    x_thres_t = recall_t[index]
    y_thres_t = prec_t[index]
    x_thres_v = recall_v[index]
    y_thres_v = prec_v[index]

    plt.figure()
    lw = 2
    plt.plot(recall_t, prec_t, color='darkorange', lw=lw, label='Testing')
    plt.plot(recall_v, prec_v, color='purple', lw=lw, label='Validation')
    plt.plot(x_thres_t, y_thres_t, color='red', lw=lw, marker='*',
             markersize=12)  # Testing threshold tirado dos vetores prec/recall usando o index de probs mais proximos do threshold = 0.7
    plt.plot(x_thres_v, y_thres_v, color='red', lw=lw, marker='*', markersize=12)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('MC1 Precision-Recall Curve')
    plt.legend(loc="lower right")
    plt.show()

    plt.savefig(fig2_name)

    pass


if __name__ == '__main__':
    main()