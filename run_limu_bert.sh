cd /home/zsarwar/cs/LIMU-BERT-Public/dataset
python3 motion_final.py \
--data_folder='/home/zsarwar/cs/datasets/ass_f/data/test_unlabeled'
cd /home/zsarwar/cs/LIMU-BERT-Public
python3 embedding.py v1 motion 20_120 -f motion
python3 classifier_final.py v2 motion 20_120 -f motion -s motion -l 0