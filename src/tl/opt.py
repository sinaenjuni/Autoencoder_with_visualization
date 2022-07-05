import torch.nn as nn
from torch.nn import init
from torch.nn.utils import spectral_norm

class ConditionalBatchNorm2d(nn.Module):
    # https://github.com/voletiv/self-attention-GAN-pytorch
    def __init__(self, in_features, out_features, MODULES):
        super().__init__()
        self.in_features = in_features
        self.bn = batchnorm_2d(out_features, eps=1e-4, momentum=0.1, affine=False)

        self.gain = MODULES.g_linear(in_features=in_features, out_features=out_features, bias=False)
        self.bias = MODULES.g_linear(in_features=in_features, out_features=out_features, bias=False)

    def forward(self, x, y):
        gain = (1 + self.gain(y)).view(y.size(0), -1, 1, 1)
        bias = self.bias(y).view(y.size(0), -1, 1, 1)
        out = self.bn(x)
        return out * gain + bias



def init_weights(modules, initialize):
    for module in modules():
        if (isinstance(module, nn.Conv2d) or isinstance(module, nn.ConvTranspose2d) or isinstance(module, nn.Linear)):
            if initialize == "ortho":
                init.orthogonal_(module.weight)
                if module.bias is not None:
                    module.bias.data.fill_(0.)
            elif initialize == "N02":
                init.normal_(module.weight, 0, 0.02)
                if module.bias is not None:
                    module.bias.data.fill_(0.)
            elif initialize in ["glorot", "xavier"]:
                init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    module.bias.data.fill_(0.)
            else:
                pass
        elif isinstance(module, nn.Embedding):
            if initialize == "ortho":
                init.orthogonal_(module.weight)
            elif initialize == "N02":
                init.normal_(module.weight, 0, 0.02)
            elif initialize in ["glorot", "xavier"]:
                init.xavier_uniform_(module.weight)
            else:
                pass
        else:
            pass


def conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
    return nn.Conv2d(in_channels=in_channels,
                     out_channels=out_channels,
                     kernel_size=kernel_size,
                     stride=stride,
                     padding=padding,
                     dilation=dilation,
                     groups=groups,
                     bias=bias)


def deconv2d(in_channels, out_channels, kernel_size, stride=2, padding=0, dilation=1, groups=1, bias=True):
    return nn.ConvTranspose2d(in_channels=in_channels,
                              out_channels=out_channels,
                              kernel_size=kernel_size,
                              stride=stride,
                              padding=padding,
                              dilation=dilation,
                              groups=groups,
                              bias=bias)


def linear(in_features, out_features, bias=True):
    return nn.Linear(in_features=in_features, out_features=out_features, bias=bias)


def embedding(num_embeddings, embedding_dim):
    return nn.Embedding(num_embeddings=num_embeddings, embedding_dim=embedding_dim)


def snconv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True):
    return spectral_norm(nn.Conv2d(in_channels=in_channels,
                                   out_channels=out_channels,
                                   kernel_size=kernel_size,
                                   stride=stride,
                                   padding=padding,
                                   dilation=dilation,
                                   groups=groups,
                                   bias=bias),
                         eps=1e-6)


def sndeconv2d(in_channels, out_channels, kernel_size, stride=2, padding=0, dilation=1, groups=1, bias=True):
    return spectral_norm(nn.ConvTranspose2d(in_channels=in_channels,
                                            out_channels=out_channels,
                                            kernel_size=kernel_size,
                                            stride=stride,
                                            padding=padding,
                                            dilation=dilation,
                                            groups=groups,
                                            bias=bias),
                         eps=1e-6)


def snlinear(in_features, out_features, bias=True):
    return spectral_norm(nn.Linear(in_features=in_features, out_features=out_features, bias=bias), eps=1e-6)


def sn_embedding(num_embeddings, embedding_dim):
    return spectral_norm(nn.Embedding(num_embeddings=num_embeddings, embedding_dim=embedding_dim), eps=1e-6)


def batchnorm_2d(in_features, eps=1e-4, momentum=0.1, affine=True):
    return nn.BatchNorm2d(in_features, eps=eps, momentum=momentum, affine=affine, track_running_stats=True)
