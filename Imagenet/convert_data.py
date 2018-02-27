import xml.etree.ElementTree as ET

import cv2

import os

import tensorflow as tf
import io

import PIL.Image

from object_detection.utils import dataset_util


flags = tf.app.flags
flags.DEFINE_string('output_path', 'person_train.record', 'Path to output TFRecord')
flags.DEFINE_string('label_map_path', 'data/person.pbtxt',
'Path to label map proto')

FLAGS = flags.FLAGS




def create_tf_example(root):

	# TODO: Populate the following variables from your example.
	height = None # Image height
	width = None # Image width
	filename = None # Filename of the image. Empty if image is not from file
	encoded_jpeg = None # Encoded image bytes
	image_format = b'jpeg'

	xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
	xmaxs = [] # List of normalized right x coordinates in bounding box
	         # (1 per box)
	ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
	ymaxs = [] # List of normalized bottom y coordinates in bounding box
	         # (1 per box)
	classes_text = [] # List of string class name of bounding box (1 per box)
	classes = [] # List of integer class id of bounding box (1 per box)


	filename = os.path.join(os.path.abspath("./data"), root[0].text, root[1].text + ".JPEG")


	with tf.gfile.GFile(filename, 'rb') as fid:
		encoded_jpg = fid.read()


	encoded_jpg_io = io.BytesIO(encoded_jpg)
	image = PIL.Image.open(encoded_jpg_io)

	if image.format != 'JPEG':
		raise ValueError('Image format not JPEG')


	img = cv2.imread(filename)
	cv2.imshow("img", img)
	cv2.waitKey(1)
	print img.shape
	height = int(root[3][0].text)
	width = int(root[3][1].text)

	'''xmins = []
	xmaxs = []
	ymins = []
	ymaxs = []
	classes_text = []
	classes = []'''

	for child in root:
	     if child.tag == "object" and child[0].text == "n07942152":
	        print child[0].tag, child[0].text, child[4][0].text, child[4][1].text, child[4][2].text, child[4][3].text
	        xmins.append(int(child[4][0].text) / float(width))
	        ymins.append(int(child[4][1].text) / float(height))
	        xmaxs.append(int(child[4][2].text) / float(width))
	        ymaxs.append(int(child[4][3].text) / float(height))
	        classes_text.append("person")
	        classes.append(1)


	print xmins, xmaxs, ymins, ymaxs, classes_text, classes


	tf_example = tf.train.Example(features=tf.train.Features(feature={
	  'image/height': dataset_util.int64_feature(height),
	  'image/width': dataset_util.int64_feature(width),
	  'image/filename': dataset_util.bytes_feature(filename),
	  'image/source_id': dataset_util.bytes_feature(filename),
	  'image/encoded': dataset_util.bytes_feature(encoded_jpg),
	  'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
	  'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
	  'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
	  'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
	  'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
	  'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
	  'image/object/class/label': dataset_util.int64_list_feature(classes),
	}))
	return tf_example


def main(_):
	writer = tf.python_io.TFRecordWriter(FLAGS.output_path)


	files = os.listdir("./data/Annotation/n07942152")
	for anns in files:
	    print anns
	    tree = ET.parse(os.path.join(os.path.abspath("./data/Annotation/n07942152"), anns))
	    root = tree.getroot()

	    tf_example = create_tf_example(root)
	    writer.write(tf_example.SerializeToString())


	writer.close()


if __name__ == '__main__':
	tf.app.run()
