python3 limu_bert/dataset/motion_final_val.py --data_folder=$1
python3 limu_bert/embedding.py v1 motion 20_120 -f motion \
	--train_cfg limu_bert/config/pretrain.json --mask_cfg limu_bert/config/mask.json
python3 limu_bert/classifier_final_val.py v2 motion 20_120 -f motion -s motion -l 0 \
	--train_cfg limu_bert/config/train.json --output_predictions=$2