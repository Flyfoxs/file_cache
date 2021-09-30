
def print_imp_list( train, clf, order_by_wight=True, show_zero=True):
    if hasattr(clf, 'feature_importances_'):
        imp_item = dict(zip(train.columns, clf.feature_importances_))

        imp_list = sorted(imp_item.items(), key=lambda imp: imp[1], reverse=True)

        # for key, value in imp_list:
        #     if value > 0:
        #         print(f'Import {value}: {key}')
        #         print(train[str(key)].dtype.name)
        #     else:
        #         print(f'zeor imp:{key}')
        #

        zero_list = [key for key, value in imp_list if value==0]

        print(f'Full List:{len(train.columns)}, Zero List:{len(zero_list)}, ')


        imp_list = [(key, value, train[key].dtype.name) for key, value in imp_list if value>0]

        if order_by_wight :
            imp_list = sorted(imp_list, key=lambda imp: imp[1], reverse=True)
        else:
            imp_list = sorted(imp_list, key=lambda imp: imp[2])

        import_sn = 0
        for (key, value, dtype) in imp_list:
            import_sn += 1
            #logger.info("%03d: %s, %s, %s" % ( import_sn, str(key).ljust(35), str(value).ljust(5), dtype))

        print(f'Full List:{len(train.columns)}, Zero List:{len(zero_list)}, ')




from functools import lru_cache
@lru_cache()
def get_gpu_paras(kind='lgb'):
    import os
    if 'CUDA_VISIBLE_DEVICES' in os.environ:
        if kind == 'lgb':
            gpu_params = {'device': 'gpu', 'gpu_platform_id': 0,'gpu_device_id': 0}
        else:
            gpu_params = {'tree_method': 'gpu_hist', 'predictor': 'gpu_predictor'}
        #logger.debug(f"GPU is enable with{kind}, :{gpu_params}")

    else:
        #logger.debug("GPU is disable")
        gpu_params = {}
    return gpu_params


from sklearn.metrics import f1_score

def lgb_f1_score(y_hat, data):
    y_true = data.get_label()
    y_hat = np.round(y_hat) # scikits f1 doesn't like probabilities
    return 'f1', f1_score(y_true, y_hat), True


def xg_f1(y,t):
    # logger.debug(f'prediction = {y.shape}')
    # logger.debug(y[:10])

    t = t.get_label()
    # logger.debug(f'label = {t.shape}')

    y_bin = [1. if y_cont > 0.5 else 0. for y_cont in y] # binaryzing your output
    return 'f1',-f1_score(t,y_bin)

def estimate_f1_score(prediction, label, verbose=True):
    result = {}
    for threshold in np.arange(0.1, 0.6, 0.05):
        threshold = round(threshold, 2)
        prediction_new = [1. if y_cont > threshold else 0. for y_cont in prediction]  # binaryzing your output
        f1 = round(f1_score(label, prediction_new),5)
        result[threshold] = f1
        if verbose:
            pass
            #logger.debug(f'threshold:{round(threshold, 2)}, f1:{round(f1, 5)}')
    result  = result.items()
    result = sorted(result, key= lambda val: val[1], reverse=True)
    return result[0]

if __name__ == '__main__' :
    pass
    #logger.debug(get_pretty_info({'feature_fraction': 0.7, 'max_depth': 8, 'reg_alpha': 0.8, 'reg_lambda': 90},))
