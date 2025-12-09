import cv2
import numpy as np

# ---- function to get 8 bitplanes ----
def bit_planes(img):
    planes=[]
    for i in range(8):
        planes.append(((img>>i)&1)*255)
    return planes

# ---- reconstruct using lowest 3 bitplanes ----
def reconstruct_low3(planes):
    rec=((planes[0]//255)<<0)+((planes[1]//255)<<1)+((planes[2]//255)<<2)
    return rec.astype(np.uint8)

# ---- load images ----
low=cv2.imread("low light.jpg",0)
bright=cv2.imread("bright light.jpg",0)

if low is None or bright is None:
    print("Image not found. Check paths.")
    exit()

# ---- LOW LIGHT PROCESS ----
low_planes=bit_planes(low)
low_rec=reconstruct_low3(low_planes)
low_diff=cv2.absdiff(low,low_rec)

cv2.imshow("Low Light - Original",low)
cv2.imshow("Low Light - Reconstructed from lowest 3",low_rec)
cv2.imshow("Low Light - Difference",low_diff)

# ---- BRIGHT LIGHT PROCESS ----
bright_planes=bit_planes(bright)
bright_rec=reconstruct_low3(bright_planes)
bright_diff=cv2.absdiff(bright,bright_rec)

cv2.imshow("Bright Light - Original",bright)
cv2.imshow("Bright Light - Reconstructed from lowest 3",bright_rec)
cv2.imshow("Bright Light - Difference",bright_diff)

cv2.waitKey(0)
cv2.destroyAllWindows()
