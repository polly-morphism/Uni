import torch


def validate(hp, args, alice, bob, eve, valloader, writer, step, epoch):
    alice.eval()
    bob.eval()
    eve.eval()

    correct_e = 0
    correct_b = 0
    for plain, key in valloader:
        plain = plain.cuda()
        key = key.cuda()
        cipher = alice(plain, key)
        outE = eve(cipher)
        outB = bob(cipher, key)
        correct_e += torch.sum(torch.abs(plain - outE) < 1).item() / hp.data.plain
        correct_b += torch.sum(torch.abs(plain - outB) < 1).item() / hp.data.plain

    acc_e = correct_e / len(valloader.dataset)
    acc_b = correct_b / len(valloader.dataset)

    writer.log_accuracy(acc_b, acc_e, step)
    print("Accuracy(%%): Bob %.1f Eve %.1f" % (100.0 * acc_b, 100.0 * acc_e))

    if epoch % 10 == 0 and epoch != 0:
        torch.save(
            {"epoch": epoch, "model_state_dict": alice.state_dict(),},
            "./nncrypt/checkpoints/alice_epoch_{}.pth".format(epoch),
        )
        torch.save(
            {"epoch": epoch, "model_state_dict": bob.state_dict(),},
            "./nncrypt/checkpoints/bob_epoch_{}_acc_{}.pth".format(
                epoch, 100.0 * acc_b
            ),
        )

        torch.save(
            {"epoch": epoch, "model_state_dict": eve.state_dict(),},
            "./nncrypt/checkpoints/eve_epoch_{}_acc_{}.pth".format(
                epoch, 100.0 * acc_e
            ),
        )

    alice.train()
    bob.train()
    eve.train()
