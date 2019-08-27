from models.yolonet import yolo_mobilev1, yolo_mobilev2, tiny_yolo, yolo,\
    yoloalgin_mobilev1, yoloalgin_mobilev2, yolov2algin_mobilev1, pfld
from tensorflow.python.keras.optimizers import Adam, SGD, RMSprop
from tools.custom import RAdam
from tools.utils import Helper, YOLO_Loss
from tools.alignutils import YOLOAlignHelper, YOLOAlign_Loss
from tools.landmarkutils import LandmarkHelper, LandMark_Loss
from yaml import safe_dump


class dict2obj(object):
    def __init__(self, dicts):
        """ convert dict to object , NOTE the `**kwargs` will not be convert 

        Parameters
        ----------
        object : [type]

        dicts : dict
            dict
        """
        for name, value in dicts.items():
            if isinstance(value, (list, tuple)):
                setattr(self, name, [dict2obj(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, name, dict2obj(value) if (isinstance(value, dict) and 'kwarg' not in name) else value)


ArgDict = {
    'mode': 'train',

    # MODEL
    'model': {
        'name': 'yolo',

        'helper': 'Helper',
        'helper_kwarg': {
            'image_ann': 'data/voc_img_ann.npy',
            'class_num': 20,
            'anchors': 'data/voc_anchor.npy',
            'in_hw': [224, 320],
            'out_hw': [[7, 10], [14, 20]],
            'validation_split': 0.1,  # vaildation_split
        },

        'network': 'yolo_mobilev2',
        'network_kwarg': {
            'alpha': 0.75  # depth_multiplier
        },


        'loss': 'YOLO_Loss',
        'loss_kwarg': {
            'obj_thresh': 0.7,
            'iou_thresh': 0.5,
            'obj_weight': 1,
            'noobj_weight': 1,
            'wh_weight': 1,
        }
    },

    'train': {
        'augmenter': False,
        'batch_size': 16,
        'pre_ckpt': None,
        'rand_seed': 10101,
        'epochs': 10,
        'log_dir': 'log',
        'debug': False,
        'verbose': 1,
        'vali_step_factor': 0.5,
        'optimizer': 'RAdam',
        'optimizer_kwarg': {
            'lr': 0.001,  # init_learning_rate
            'beta_1': 0.9,
            'beta_2': 0.999,
            'epsilon': None,
            'decay': 0.  # learning_rate_decay_factor
        },
        'Lookahead': True,
        'Lookahead_kwarg': {
            'k': 5,
            'alpha': 0.5,
        },
        'earlystop': True,
        'earlystop_kwarg': {
            'monitor': 'val_loss',
            'min_delta': 0,
            'patience': 4,
            'verbose': 0,
            'mode': 'auto',
            'baseline': None,
            'restore_best_weights': False,
        },
    },

    'prune': {
        'is_prune': False,
        'init_sparsity': 0.5,  # prune initial sparsity range = [0 ~ 1]
        'final_sparsity': 0.9,  # prune final sparsity range = [0 ~ 1]
        'end_epoch': 5,  # prune epochs NOTE: must < train epochs
        'frequency': 100,  # how many steps for prune once
    }
}


helper_register = {
    'Helper': Helper,
    'YOLOAlignHelper': YOLOAlignHelper,
    'LandmarkHelper': LandmarkHelper
}


network_register = {
    'yolo_mobilev1': yolo_mobilev1,
    'yolo_mobilev2': yolo_mobilev2,
    'tiny_yolo': tiny_yolo,
    'yolo': yolo,
    'yoloalgin_mobilev1': yoloalgin_mobilev1,
    'yoloalgin_mobilev2': yoloalgin_mobilev2,
    'yolov2algin_mobilev1': yolov2algin_mobilev1,
    'pfld': pfld
}

loss_register = {
    'YOLO_Loss': YOLO_Loss,
    'YOLOAlign_Loss': YOLOAlign_Loss,
    'LandMark_Loss': LandMark_Loss
}

optimizer_register = {
    'Adam': Adam,
    'SGD': SGD,
    'RMSprop': RMSprop,
    'RAdam': RAdam
}


if __name__ == "__main__":
    with open('config/default.yml', 'w') as f:
        safe_dump(ArgDict, f, sort_keys=False)
