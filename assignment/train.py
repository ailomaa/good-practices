#!/usr/bin/env python3
"""Train a small neural network on synthetic data.

The point of this script is not the model. It is something that runs long
enough to be worth putting on a server, and that reports which machine and
which device it ran on.
"""

import argparse
import os
import socket
import time

import torch
from torch import nn


def parse_args():
    parser = argparse.ArgumentParser(description="Train a small model.")
    parser.add_argument("--epochs", type=int, default=200,
                        help="how many passes over the data (default: 200)")
    parser.add_argument("--samples", type=int, default=50000,
                        help="how many training examples to generate")
    parser.add_argument("--out", default="results/loss.csv",
                        help="where to write the loss curve")
    return parser.parse_args()


def main():
    args = parse_args()

    # Use the GPU when there is one, otherwise fall back to the CPU, so the
    # same script runs on a laptop and on the server.
    if torch.cuda.is_available():
        device = torch.device("cuda")
        device_name = f"cuda ({torch.cuda.get_device_name(0)})"
    else:
        device = torch.device("cpu")
        device_name = "cpu (no GPU found)"

    print(f"host:   {socket.gethostname()}")
    print(f"torch:  {torch.__version__}")
    print(f"device: {device_name}", flush=True)

    torch.manual_seed(0)
    x = torch.randn(args.samples, 20, device=device)
    true_w = torch.randn(20, 1, device=device)
    y = x @ true_w + 0.1 * torch.randn(args.samples, 1, device=device)

    model = nn.Sequential(
        nn.Linear(20, 256), nn.ReLU(),
        nn.Linear(256, 256), nn.ReLU(),
        nn.Linear(256, 1),
    ).to(device)

    loss_fn = nn.MSELoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)

    start = time.time()
    history = []
    for epoch in range(1, args.epochs + 1):
        optimiser.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimiser.step()

        history.append((epoch, loss.item()))
        if epoch % 100 == 0 or epoch == 1:
            print(f"epoch {epoch:6d}  loss {loss.item():.4f}", flush=True)

    print(f"done in {time.time() - start:.1f} s")

    out_dir = os.path.dirname(args.out) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w") as f:
        f.write("epoch,loss\n")
        for epoch, value in history:
            f.write(f"{epoch},{value:.6f}\n")

    model_path = os.path.join(out_dir, "model.pt")
    torch.save(model.state_dict(), model_path)
    print(f"wrote {args.out} and {model_path}")


if __name__ == "__main__":
    main()
