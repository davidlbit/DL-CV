from dataclasses import dataclass
import torch
import pickle
import PIL.Image
import numpy as np
import matplotlib.pyplot as plt 


outdir = "out"

V1 = "./out/latents/projected_w_alex.npz"
V2 = "./out/latents/projected_w_karol2.npz"

V3 = "./out/latents/projected_w_david.npz"
V4 = "./out/latents/chris.npz"

v1_type = "Alex"
v2_type = "Karol"
v3_type = "David"
v4_type = "Chris"



v1 = np.load(V1)['w']
v2 = np.load(V2)['w']
v3 = np.load(V1)['w']
v4 = np.load(V2)['w']

# print(torch.tensor(v1))
v1 = torch.tensor(v1).cuda()
v2 = torch.tensor(v2).cuda()
v3 = torch.tensor(v3).cuda()
v4 = torch.tensor(v4).cuda()


# # https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/ffhq.pkl
with open('model/ffhq.pkl', 'rb') as f:
    G = pickle.load(f)['G_ema'].cuda()  # torch.nn.Module
z = torch.randn([1, G.z_dim]).cuda()    # latent pytcodes
c = None                                # class labels (not used in this example)
# img = G(z, c)                           # NCHW, float32, dynamic range [-1, +1]

assert v1.shape[1:] == (G.num_ws, G.w_dim)


w_mix = 1/4*(v1+v2+v3+v4)

for idx, w in enumerate(w_mix):
    img = G.synthesis(w.unsqueeze(0), noise_mode="const")
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    x_v1 = img[0].cpu().numpy()
    img = PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB').save(f'{outdir}/interpolation_mix.png')

# fig = plt.figure(figsize=(20,20))
# subplots = [plt.subplot(2, 5, k+1) for k in range(10)]
# subplots[0].imshow(x_v1)
# subplots[0].set_title(v1_type)
# subplots[0].axis('off')

# subplots[9].imshow(x_v2)
# subplots[9].set_title(v2_type)
# subplots[9].axis('off')
# for k in range(1,9):
#     x_k = G.synthesis(torch.lerp(v1[0].unsqueeze(0),v2[0].unsqueeze(0),k/10), noise_mode="const")
#     x_k = (x_k.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
#     subplots[k].imshow(x_k[0].cpu().numpy())
#     subplots[k].set_title('Interpolation')
#     subplots[k].axis('off')
# # set the spacing between subplots
# plt.subplots_adjust(left=0.1,
#                     bottom=0.1, 
#                     right=0.9, 
#                     top=0.4, 
#                     wspace=0.1, 
#                     hspace=0.1)
# plt.savefig(f"out/interpolation_{v1_type}_{v2_type}.png",bbox_inches="tight")


