import sys


block_a_W = \
" \    \n\
  \   \n\
   \  \n\
    \ \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    / \n\
   /  \n\
  /   \n\
 /    "

block_a_D = \
" \    \n\
  \   \n\
   \  \n\
    \ \n\
|\  | \n\
|:\ | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| | \n\
|:| / \n\
|:|/  \n\
|:/   \n\
|/    "

block_a_H = \
"      \n\
      \n\
      \n\
 ___  \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
    | \n\
 ___| \n\
      \n\
      \n\
      \n\
      "

block_b_W = \
"    \n\
    \n\
    \n\
    \n\
\   \n\
 \  \n\
  \ \n\
  | \n\
  | \n\
  | \n\
  | \n\
  | \n\
  / \n\
 /  \n\
/   \n\
    \n\
    \n\
    \n\
    "

block_b_D = \
"    \n\
    \n\
    \n\
    \n\
\   \n\
 \  \n\
  \ \n\
:.| \n\
::| \n\
::| \n\
::| \n\
::| \n\
::/ \n\
:/  \n\
/   \n\
    \n\
    \n\
    \n\
    "

block_b_H = \
"    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
__  \n\
  | \n\
  | \n\
  | \n\
  | \n\
__| \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    "

block_c_W = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
\  \n\
 \ \n\
 | \n\
 | \n\
/  \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_c_D = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
\  \n\
 \ \n\
:| \n\
:| \n\
/  \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_c_H = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
_  \n\
 | \n\
_| \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_f_W = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
__ \n\
   \n\
__ \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_f_D = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
__ \n\
:: \n\
:: \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_f_H = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_e_W = \
"       \n\
       \n\
       \n\
       \n\
       \n\
       \n\
______ \n\
       \n\
       \n\
       \n\
       \n\
______ \n\
       \n\
       \n\
       \n\
       \n\
       \n\
       \n\
       "

block_e_D = \
"       \n\
       \n\
       \n\
       \n\
       \n\
       \n\
______ \n\
       \n\
 .--.  \n\
 |::|  \n\
 |::|  \n\
_|::|_ \n\
       \n\
       \n\
       \n\
       \n\
       \n\
       \n\
       "

block_d_W = \
"             \n\
             \n\
             \n\
____________ \n\
             \n\
             \n\
             \n\
             \n\
             \n\
             \n\
             \n\
             \n\
             \n\
             \n\
____________ \n\
             \n\
             \n\
             \n\
             "

block_d_D = \
"             \n\
             \n\
             \n\
____________ \n\
             \n\
   .----.    \n\
  /::::::\   \n\
 |::....::|  \n\
 |::....::|  \n\
 |:......:|  \n\
 |:......:|  \n\
 |:......:|  \n\
 |:......:|  \n\
 |:......:|  \n\
_|:......:|_ \n\
             \n\
             \n\
             \n\
             "

block_i_W = \
"   / \n\
  /  \n\
 /   \n\
/    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
|    \n\
\    \n\
 \   \n\
  \  \n\
   \ "

block_i_D = \
"   / \n\
  /   \n\
 /    \n\
/     \n\
|  /| \n\
| /:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
| |:| \n\
\ |:| \n\
 \|:| \n\
  \:| \n\
   \| "


block_i_H = \
"      \n\
      \n\
      \n\
 ____ \n\
|     \n\
|     \n\
|     \n\
|     \n\
|     \n\
|     \n\
|     \n\
|     \n\
|     \n\
|     \n\
|____ \n\
      \n\
      \n\
      \n\
      "

block_h_W = \
"    \n\
    \n\
    \n\
    \n\
  / \n\
 /  \n\
/   \n\
|   \n\
|   \n\
|   \n\
|   \n\
|   \n\
\   \n\
 \  \n\
  \ \n\
    \n\
    \n\
    \n\
    "

block_h_H = \
"     \n\
     \n\
     \n\
     \n\
     \n\
     \n\
 ___ \n\
|    \n\
|    \n\
|    \n\
|    \n\
|___ \n\
     \n\
     \n\
     \n\
     \n\
     \n\
     \n\
     "

block_h_D = \
"    \n\
    \n\
    \n\
    \n\
  / \n\
 /  \n\
/   \n\
|.: \n\
|:: \n\
|:: \n\
|:: \n\
|:: \n\
\:: \n\
 \: \n\
  \ \n\
    \n\
    \n\
    \n\
    "

block_g_W = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
 / \n\
/  \n\
|  \n\
|  \n\
 \ \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "

block_g_H = \
"    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
 __ \n\
|   \n\
|__ \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    \n\
    "

block_g_D = \
"   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
 / \n\
/  \n\
|: \n\
|: \n\
 \ \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   \n\
   "


# Given a set of image names, put together their corresponding images in order from a -> i
def build_view(image_parts):

    ordered_parts = sorted(image_parts)

    prep_buff = []
    finished = []
    for part_name in ordered_parts:
        # Get the image from the name
        part = getattr(sys.modules[__name__], part_name)
        # Convert Image into rows of strings
        prep_buff.append(str.splitlines(part))

    for index in range(19):
        line = ''
        for prepped_part in prep_buff:
            line += prepped_part[index][:-1]
        finished.append(line)

    finished_image = ''
    for line in finished:
        finished_image += line + '\n'
    return finished_image


if __name__ == "__main__":
    # Testing
    long_hallway = build_view([
        'block_a_W',
        'block_b_D',
        'block_h_W',
        'block_f_W',
        'block_g_H',
        'block_c_W',
        'block_i_W']
    )

    print(long_hallway)
