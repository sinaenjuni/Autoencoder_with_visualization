import torch
import torch.nn as nn
from models.modules.encoder import Encoder
from models.modules.decoder import Decoder


class AE(nn.Module):
    def __init__(self, image_size, image_channel, std_channel, latent_dim, norm):
        super(AE, self).__init__()
        self.encoder = Encoder(image_size=image_size,
                                image_channel=image_channel,
                                std_channel=std_channel,
                                latent_dim=latent_dim,)
        self.decoder = Decoder(image_size=image_size,
                                image_channel=image_channel,
                                std_channel=std_channel,
                                latent_dim=latent_dim,
                               norm=norm)
    def forward(self, x):
        encode = self.encoder(x)
        decode = self.decoder(encode)
        return decode


if __name__ == "__main__":
    ae = AE(image_size=64, image_channel=3, std_channel=64, latent_dim=128, norm='bn')
    # print(list(ae.encoder.modules()))
    # print(ae.encoder.layer2[0].weight)