# Endireita a tela do iPad do post 057_1 (cantos marcados à mão sobre a foto em 720 px) -> ryu-plano.png
import cv2, numpy as np
im = cv2.imread('../../../_ref/ig/057_1.jpg'); k = im.shape[1] / 720
q = np.float32([[62, 33], [598, 42], [712, 903], [6, 903]]) * k
W, H = 1400, 1960
M = cv2.getPerspectiveTransform(q, np.float32([[0, 0], [W, 0], [W, H], [0, H]]))
cv2.imwrite('ryu-plano.png', cv2.warpPerspective(im, M, (W, H), flags=cv2.INTER_CUBIC))
