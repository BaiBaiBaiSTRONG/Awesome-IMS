import paddlehub as hub

def run_moudle(img_path):
    module = hub.Module(name='xception65_imagenet')

    input_dict = {'image': [img_path]}
    result = module.classification(data=input_dict)
    print(result)
    return list(result[0][0].keys()), list(result[0][0].values())

if __name__ == "__main__":
    a, b = run_moudle('../static/img/welcom.jpg')
    print(a)
    print(b)
