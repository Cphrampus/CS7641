Code Location: https://github.gatech.edu/cphrampus3/CS7641.git
Running code:

- Project code in folder `P1-SL`
- Initial learning curves were generated using sklearn defaults, nothing but random_state=0
    - DT used criterion="entropy", since that is the one covered in lectures
    - random_state not applicable for KNN
- Requirements were pip frozen to requirements.txt
- `python main.py`
    - run all classifiers across both datasets
    - save charts to `charts/<classifier name>_<dataset #>_final_<learn|val|conf_matrix>_<timestamp to avoid overwrites>`
- if final test set scoring is desired, the `False` on line 963 should be changed to `True`