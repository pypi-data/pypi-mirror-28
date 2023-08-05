import numpy as np
import matplotlib.pyplot as plt


def get_color_for_layeridx(layeridx):
    base6_colors = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1]]
    if layeridx < 6:
        return base6_colors[layeridx]
    else:
        ro = 77
        bo = 91
        go = 111
        if layeridx%3 == 0:
            return [((layeridx-5)*ro %255)/255, ((layeridx-6)*bo %255)/255, ((layeridx-6)*go %255)/255]
        elif layeridx%3 == 1:
            return [((layeridx-6) * ro % 255) / 255, ((layeridx-5) * bo % 255) / 255, ((layeridx-6) * go % 255) / 255]
        else:
            return [((layeridx-6) * ro % 255) / 255, ((layeridx-6) * bo % 255) / 255, ((layeridx-5) * go % 255) / 255]

############################
# # TEST

# img = np.zeros((10,10,3))
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         img[i,j] = get_color_for_layeridx(i*img.shape[1]+j)
# fig, ax = plt.subplots()
# ax.imshow(img, cmap='gray',interpolation='nearest', origin='upper')
# plt.show()
