import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def spatial_filtering_raw(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Could not read image:", image_path)
        return

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = {'Original': img_rgb}
    
    # --- Box Filters ---
    for size in [5, 20]:
        # Normalized (Preserves brightness)
        results[f'Box {size}x{size} (Norm)'] = cv2.boxFilter(img_rgb, -1, (size, size), normalize=True)
        
        # Unnormalized (Raw summation - will look white/bright)
        # We use float32 to prevent clipping at 255 during math
        results[f'Box {size}x{size} (Unnorm)'] = cv2.boxFilter(img_rgb, cv2.CV_32F, (size, size), normalize=False)

    # --- Gaussian Filter Calculations ---
    sigma = 3.0
    ksize = int(2 * math.ceil(3 * sigma) + 1)
    
    center = ksize // 2
    x = np.linspace(-center, center, ksize)
    kernel_1d = np.exp(-(x**2) / (2 * sigma**2))
    
    # Normalized Kernel
    k_norm = kernel_1d / np.sum(kernel_1d)
    
    # A. Normalized Gaussian
    results[f'Gauss (Norm)'] = cv2.sepFilter2D(img_rgb, -1, k_norm, k_norm)
    
    # B. Unnormalized Gaussian (Raw math)
    results[f'Gauss (Unnorm)'] = cv2.sepFilter2D(img_rgb, cv2.CV_32F, kernel_1d, kernel_1d)

    # --- Plotting ---
    plt.figure(figsize=(15, 8))
    for i, (label, image) in enumerate(results.items()):
        plt.subplot(2, 4, i + 1)
        # We display the raw float image. 
        # Matplotlib clips float values > 1.0 to white, 
        # showing exactly how "blown out" unnormalized filters are.
        plt.imshow(image.astype(np.uint8) if image.dtype != 'float32' else image / 255.0)
        plt.title(label)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

spatial_filtering_raw('Torgya - Arunachal Festival.jpg')
