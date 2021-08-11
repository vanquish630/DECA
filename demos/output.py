# -*- coding: utf-8 -*-
#
# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# Using this computer program means that you agree to the terms
# in the LICENSE file included with this software distribution.
# Any use not explicitly granted by the LICENSE is prohibited.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# For comments or questions, please email us at deca@tue.mpg.de
# For commercial licensing contact, please contact ps-license@tuebingen.mpg.de

import os, sys
import cv2
import numpy as np
from time import time
from scipy.io import savemat
import argparse
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decalib.deca import DECA
from decalib.datasets import datasets
from decalib.utils import util
from decalib.utils.config import cfg as deca_cfg
from decalib.models.FLAME import FLAME, FLAMETex
from decalib.utils.renderer import SRenderY


def main(args):
    device = 'cpu'
    # load test images
    params = np.load(args.inputpath,allow_pickle=True).item()
    #print(params['shape'][0])
    start_time = time()

    flame = FLAME(deca_cfg.model).to(device)
    flametex = FLAMETex(deca_cfg.model).to(device)

    verts, landmarks2d, landmarks3d = flame(shape_params=params['shape'], expression_params=params['exp'],
                                             pose_params=params['pose'])
    albedo = flametex(params['tex'])
    print(f'\nDuration: {time() - start_time:.0f} seconds')  # print the time elapsed
    opdict = {
        'vertices': verts,
        'landmarks2d': landmarks2d,
        'landmarks3d': landmarks3d,
        'albedo':albedo
    }
    render = SRenderY(256, obj_filename=deca_cfg.model.topology_path, uv_size=deca_cfg.model.uv_size).to(device)

    vertices = opdict['vertices'][0].cpu().numpy()
    faces = render.faces[0].cpu().numpy()
    texture = util.tensor2image(opdict['albedo'][0])
    util.write_obj("Tests/test_zje", vertices, faces)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DECA: Detailed Expression Capture and Animation')

    parser.add_argument('-i', '--inputpath', default='Results', type=str,
                        help='path to the test data, can be image folder, image path, image list, video')

    main(parser.parse_args())