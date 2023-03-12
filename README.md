# ������ ���� � ����� tululu.org

������ ���������-������ ��������� ���������������� ������� ���������� ���� �� ���������� [tululu.org](https://tululu.org/)

### ��� ����������

Python3 ������ ���� ��� ����������. ����� ����������� pip ��� ��������� ������������:

```pip install -r requirements.txt```

### ���������
��������� �������� ����� ��������� ����������� ������ - 
`tululu.py`  � `parse_tululu_category.py`.
������� ����������� � ���, ��� ������ `tululu.py`  ��������� ��� ����� � �������� ��������� (��. �������� ����),
� ������ `parse_tululu_category.py` ����� ��������� ����� �������� ������� "������� ����������" ����������.
����� ����, `parse_tululu_category.py` �������� ���������������� ������� � �������� ������� ����� ���������� (��. �������� ����).

##### tululu.py
��� ������� ����� - `tululu.py` �� ������ ������������ ��������� ���������:
* `--start_page` - ID (�������������) �����, � ������� ��������� ������ ����������. ����������� ������ `-s`
* `--end_page` - ID (�������������) �����, �� ������� ���������� ���������� (�� ������� �). ����������� ������ `-e`

������ ��� ������� ���������� ���� � 1 �� 5 ID:

```python tululu.py -s 1 -e 6```, ��� ������������: 

```python tululu.py --start_page 1 --end_page 6```
##### parse_tululu_category.py

��� ������� ����� - `parse_tululu_category.py` �� ������ ������������ ��������� ���������:
###### ��� ��������� ��������� �������� ���������������.

* `--start_page` - ����� ��������, � ������� ��������� ������ ����������. ����������� ������ `-sp`. ��� - int(����� �����). �� ��������� 1.
* `--end_page` - ����� ��������, �� ������� ��������� �������� ���������� (�� ������� �). ����������� ������ `-ep` ��� - int(����� �����). �� ��������� 5
* `--dest_folder` - ���� �� "�������" ���������� �������. ������ � ������ ���������� ��������� ����� ��������� ��������� ������: ����� � �������� � ��� � ��������������� ���������� books, img, � ����� ������ � ������� json. ����������� ������ `-df`. ��� - string(������).
�� ��������� ������� ����������� �������� ����������, ��� ������������� ������ `parse_tululu_category.py`
* `--skip_txt` - � ������ ������� ������� � ������ ���������� (��������� �������������� �������� �� �����) ��������� �� ��������� ����������� ������� ����. �� ��������� ���������� ��������.
* `--skip_imgs` - � ������ ������� ������� � ������ ���������� (��������� �������������� �������� �� �����) ��������� �� ��������� ��������� ����� ����. �� ��������� ���������� ��������.
* `--json_path` - ���� �� ����� json, � ������� ����� �������� ������ � ����������� ��������. ��� ���� �� ����� ��������� ���������� ����� .json, ������ ������� ��� �������������. ����������� ������ `-jp`. ��� - string(������). 
�� ��������� ���� ���������� � ���������� �� �������� ���� (� ������ �������� �����) � �������� � ������� `--dest_folder` ����������. ��� ����� �� ��������� - `books.json`.

������ ��� ������� ���������� ������� � 1 �� 5 (������������):

```python parse_tululu_category.py -sp 1 -ep 6```, ��� ������������: 

```python parse_tululu_category.py --start_page 1 --end_page 6```

### ���� �������

��� ������� � ��������������� ����� �� ������-����� ��� ���-������������� [dvmn.org](https://dvmn.org/).****