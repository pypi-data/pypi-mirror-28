import click


@click.command()
@click.option('--input', '-i', type=str)
@click.option('--output', '-o', type=str)
@click.option('--skip_keys', '-s', type=str)
@click.option('--phantom_x', '-x', type=int)
@click.option('--phantom_y', '-y', type=int)
@click.option('--sen_width', '-w', type=float)
def reconnpz(input, output, skip_keys, phantom_x, phantom_y, sen_width):
    from dxpy.tensor.io import load_npz
    from tqdm import tqdm
    sinos = load_npz(input)
    result = {k: [] for k in sinos} 
    nb_imgs = None
    for k in sinos:
        if k == skip_keys:
            result[k] = sinos[k]
            continue
        if nb_imgs is None:
            nb_imgs = sinos[k].shape[0]
        else:
            if not nb_imgs == sinos[k].shape[0]:
                raise ValueError("Invalid sinos shape.")
        

        
