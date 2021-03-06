# -*- coding: utf-8 -*-
#from config import *


# Return list of lists [category_id, 'category_name_string', category_type_id]
def get_category_id_name_type(path_list_attr_cloth):
    category_list = []
    with codecs.open(path_list_attr_cloth, 'r', 'utf-8') as file_list_attr_clothes:
        next(file_list_attr_clothes)
        next(file_list_attr_clothes)
        for idx, line in enumerate(file_list_attr_clothes, 1):
            category_name = line[24:66].strip().replace(' ', '_').upper()
            category_attribute_type = int(line[-5:].strip())
            category_list.append([idx, category_name, category_attribute_type])
    return category_list


# Return dictionary attr_type_dict = {'category_type_id': 'category_type_name'}
def generate_attr_type_dict(path_list_attr_type):
    attr_type_dict = dict()
    with codecs.open(path_list_attr_type, 'r', 'utf-8') as file_list_attr_clothes:
        next(file_list_attr_clothes)
        next(file_list_attr_clothes)
        for idx, line in enumerate(file_list_attr_clothes, 1):
            attr_type_name = line[-37:].strip().replace(' ', '_').upper()
            attr_type_dict[idx] = attr_type_name
    return attr_type_dict


# merge into list of lists [category_id, 'category_name_string', category_type_id, 'category_type_id']
def merge_attr_types_names(attr_type_dict, category_list):
    for category_id in category_list:
        category_id.append(attr_type_dict[category_id[-1]])
    return category_list


# build three sets with unique item ids according to train/test/eval partition
def get_item_ids_partition_sets(path_list_eval_partition):
    train_ids = set()
    val_ids = set()
    test_ids = set()
    with codecs.open(path_list_eval_partition, 'r', 'utf-8') as file_list_eval_partition:
        next(file_list_eval_partition)
        next(file_list_eval_partition)
        for line in file_list_eval_partition:
            if line.split()[3] == 'train':
                train_ids.add(line.split()[2])
            elif line.split()[3] == 'val':
                val_ids.add(line.split()[2])
            else:
                test_ids.add(line.split()[2])
    return train_ids, val_ids, test_ids


def gen_processed_list_eval_partition(path_list_eval_partition):
    df_list_eval_partition = pd.read_table(path_list_eval_partition,
                                           delim_whitespace=True, skiprows=0, header=1)
    consumer_files = df_list_eval_partition.drop('image_pair_name_2', axis=1).drop_duplicates()
    consumer_files = consumer_files.rename(columns={'image_pair_name_1': 'image_name'})
    shop_files = df_list_eval_partition.drop('image_pair_name_1', axis=1).drop_duplicates()
    shop_files = shop_files.rename(columns={'image_pair_name_2': 'image_name'})
    processed_list_eval_partition = consumer_files.append(shop_files, ignore_index=True)
    return processed_list_eval_partition


def gen_full_anno(path_list_eval_partition, path_list_landmarks_consumer2shop,
                  path_list_bbox_consumer2shop, path_list_attr_items,
                  bbox=True, item_features = True):
    processed_list_eval_partition = gen_processed_list_eval_partition(path_list_eval_partition)
    landmarks_consumer2shop = pd.read_table(path_list_landmarks_consumer2shop,
                                            delim_whitespace=True, skiprows=0, header=1)
    full_anno = processed_list_eval_partition.merge(landmarks_consumer2shop,
                                                    how='inner', on='image_name')
    if bbox:
        bbox_consumer2shop = pd.read_table(path_list_bbox_consumer2shop,
                                                delim_whitespace=True, skiprows=0, header=1)
        full_anno = full_anno.merge(bbox_consumer2shop, how='inner', on='image_name')
    if item_features:
        col = ['item_id'] + ['Attr' + str(i) for i in range(1, 304)]
        attr_consumer2shop = pd.read_table(path_list_attr_items,
                                                delim_whitespace=True, skiprows=2, header=None, names=col)
        full_anno = full_anno.merge(attr_consumer2shop,how='outer', on='item_id', validate="m:1")
    return full_anno


def split_full_anno(df_full_anno):
    train = df_full_anno[df_full_anno.evaluation_status == 'train']
    eval = df_full_anno[df_full_anno.evaluation_status == 'eval']
    test = df_full_anno[df_full_anno.evaluation_status == 'test']
    return train, eval, test



if __name__ == '__main__':

    category_list = get_category_id_name_type(list_attr_cloth)
    attr_type_dict = generate_attr_type_dict(list_attr_type)
    category_data = merge_attr_types_names(attr_type_dict, category_list)
    train_ids_set, val_ids_set, test_ids_set = get_item_ids_partition_sets(list_eval_partition)
    df_full_anno = gen_full_anno(list_eval_partition, list_landmarks_consumer2shop,
                  list_bbox_consumer2shop, list_attr_items, item_features= True)
    df_train, df_eval, df_test = split_full_anno(df_full_anno)


    #########################################################################
    train = df_train.image_name.tolist()

    del(df_train, df_full_anno,df_eval,df_test)

    t0 = time.time()
    data_train = [(Image.open(fname)) for fname in train[0:50000]]
    with open('data_train.pkl', 'wb') as f:
        pickle.dump(data_train, f)
    (time.time() - t0)
print(sys.getsizeof(data_train))





with open('data_train.pkl', 'rb') as f:
    data_train = pickle.load(f)