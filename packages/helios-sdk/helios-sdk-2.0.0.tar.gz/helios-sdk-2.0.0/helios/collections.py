"""
SDK for the Helios Collections API.

Methods are meant to represent the core functionality in the developer
documentation.  Some may have additional functionality for convenience.

"""
import hashlib
import logging
from contextlib import closing
from itertools import repeat
from multiprocessing.pool import ThreadPool

from helios.core import SDKCore, IndexMixin, ShowMixin, ShowImageMixin, \
    DownloadImagesMixin, RequestManager
from helios.utilities import logging_utils


class Collections(DownloadImagesMixin, ShowImageMixin, ShowMixin, IndexMixin, SDKCore):
    """
    The Collections API allows users to group and organize individual image
    frames.

    Collections are intended to be short-lived resources and will be accessible
    for 90 days from the time the collection was created. After that time
    period has expired, the collection and all associated imagery will be
    removed from the system.

    """
    core_api = 'collections'
    max_threads = 32

    def __init__(self):
        self.request_manager = RequestManager(pool_maxsize=self.max_threads)
        self.logger = logging.getLogger(__name__)

    def index(self, **kwargs):
        """
        Return a list of collections matching the provided spatial, text, or
        metadata filters.

        The maximum skip value is 4000. If this is reached, truncated results
        will be returned. You will need to refine your query to avoid this.

        Args:
            **kwargs: Any keyword arguments found in the documentation.

        Returns:
             list: GeoJSON feature collections.

        """
        return super(Collections, self).index(**kwargs)

    def show(self, collection_id, limit=200, marker=None):
        """
        Return the attributes and image list for a single collection.

        The results will also contain image names available in the collection.
        These are limited to a maximum of 200 per query.

        Args:
            collection_id (str): Collection ID.
            limit (int, optional): Number of image names to be returned with
                each response. Defaults to 200. Max value of 200 is allowed.
            marker (str, optional): Pagination marker. If the marker is an
                exact match to an existing image, the next image after the
                marker will be the first image returned. Therefore, for normal
                linked list pagination, specify the last image name from the
                current response as the marker value in the next request.
                Partial file names may be specified, in which case the first
                matching result will be the first image returned.

        Returns:
            dict: Dictionary containing collection attributes and image list.

        """
        return super(Collections, self).show(collection_id,
                                             limit=limit,
                                             marker=marker)

    @logging_utils.log_entrance_exit
    def create(self, name, description, tags=None):
        """
        Create a new collection.

        Args:
            name (str): Display name for the collection.
            description (str): Description for the collection.
            tags (str or sequence of strs, optional): Optional comma-delimited
                keyword tags to be added to the collection.

        Returns:
            str: New collection ID.

        """
        # need to strip out the Bearer to work with a POST for collections
        post_token = self.request_manager.auth_token['value'].replace('Bearer ', '')

        # handle more than one tag
        if isinstance(tags, (list, tuple)):
            tags = ','.join(tags)

        # Compose parms block
        parms = {'name': name, 'description': description}
        if tags is not None:
            parms['tags'] = tags
        parms['access_token'] = post_token

        header = {'name': 'Content-Type',
                  'value': 'application/x-www-form-urlencoded'}

        post_url = '{}/{}'.format(self.base_api_url, self.core_api)

        resp = self.request_manager.post(post_url, headers=header, data=parms).json()

        return resp['collection_id']

    @logging_utils.log_entrance_exit
    def update(self, collections_id, name=None, description=None, tags=None):
        """
        Update a collection.

        Args:
            collections_id (str): Collection ID.
            name (str, optional): Name to be changed to.
            description (str, optional): Description to be changed to.
            tags (str or sequence of strs, optional): Optional comma-delimited
                keyword tags to be changed to.

        """
        if name is None and description is None and tags is None:
            raise ValueError('Update requires at least one named argument.')

        # need to strip out the Bearer to work with a PATCH for collections
        patch_token = self.request_manager.auth_token['value'].replace('Bearer ', '')

        # handle more than one tag
        if isinstance(tags, (list, tuple)):
            tags = ','.join(tags)

        # Compose parms block
        parms = {}
        if name is not None:
            parms['name'] = name
        if description is not None:
            parms['description'] = description
        if tags is not None:
            parms['tags'] = tags
        parms['access_token'] = patch_token

        header = {'name': 'Content-Type',
                  'value': 'application/x-www-form-urlencoded'}

        patch_url = '{}/{}/{}'.format(self.base_api_url,
                                      self.core_api,
                                      collections_id)

        self.request_manager.patch(patch_url, headers=header, data=parms)

    @logging_utils.log_entrance_exit
    def images(self, collection_id, camera=None, old_flag=False):
        """
        Returns all image names in a given collection.

        When using the optional camera input parameter only images from that
        camera will be returned.

        Args:
            collection_id (str): Collection ID.
            camera (str, optional): Camera ID to be found.
            old_flag (bool, optional): Flag for finding old format image names.
                When True images that do not contain md5 hashes at the start of
                their name will be found.

        Returns:
            sequence of strs: Image names.

        """
        max_limit = 200
        mark_img = ''

        if camera is not None:
            md5_str = hashlib.md5(camera.encode('utf-8')).hexdigest()
            if not old_flag:
                camera = md5_str[0:4] + '-' + camera
            mark_img = camera

        good_images = []
        while True:
            results = self.show(collection_id,
                                limit=max_limit,
                                marker=mark_img)

            # Gather images.
            images_found = results['images']

            if camera is not None:
                imgs_found_temp = [x for x in images_found if x.split('_')[0] == camera]
            else:
                imgs_found_temp = images_found

            if not imgs_found_temp:
                break

            good_images.extend(imgs_found_temp)
            if len(imgs_found_temp) < len(images_found):
                break
            else:
                mark_img = good_images[-1]

        return good_images

    def show_image(self, collection_id, image_names, check_for_duds=False):
        """
        Return image URLs from a collection.

        Args:
            collection_id (str): Collection ID.
            image_names (str or sequence of strs): Image names.
            check_for_duds (bool, optional): Flag for the removal of dud
                images. Defaults to False.

        Returns:
            sequence of strs: Image URLs.

        """
        return super(Collections, self).show_image(
            collection_id, image_names, check_for_duds=check_for_duds)

    @logging_utils.log_entrance_exit
    def add_image(self, collection_id, data):
        """
        Add images to a collection.

        Args:
            collection_id (str): Collection ID.
            data (dict or sequence of dicts): Data containing any of these
                payloads (camera_id), (camera_id, time), (observation_id),
                (collection_id, image). E.g. data =
                [{'camera_id': 'cam_01', time: '2017-01-01T00:00:000Z'}]

        Returns:
            If errors do occur then the data that caused the errors will be
            returned.

        """
        assert isinstance(data, (list, tuple, dict))

        # Force iterable.
        if isinstance(data, dict):
            data = [data]

        n_images = len(data)

        # Get number of threads
        num_threads = min(self.max_threads, n_images)

        # Process data.
        if num_threads > 1:
            with closing(ThreadPool(num_threads)) as thread_pool:
                results = thread_pool.map(self.__add_image_worker,
                                          zip(repeat(collection_id), data))
        else:
            results = self.__add_image_worker((collection_id, data[0]))

        # Extract failures.
        failures = [y for x, y in zip(results, data) if x == -1]

        # Determine how many were successful
        n_successful = n_images - len(failures)
        message = 'addImage({} out of {} successful)'.format(n_successful, n_images)

        if n_successful == 0:
            self.logger.error(message)
            return -1
        elif n_successful < n_images:
            self.logger.warning(message)
        else:
            self.logger.info(message)

        return failures

    def __add_image_worker(self, args):
        collection_id, payload = args

        # need to strip out the Bearer to work with a POST for collections
        post_token = self.request_manager.auth_token['value'].replace('Bearer ', '')

        # Compose post request
        parms = {'access_token': post_token}
        parms.update(payload)

        header = {'name': 'Content-Type',
                  'value': 'application/x-www-form-urlencoded'}
        post_url = '{}/collections/{}/images'.format(self.base_api_url,
                                                     collection_id)

        try:
            self.request_manager.post(post_url, headers=header, data=parms)
        except Exception:
            return -1

    @logging_utils.log_entrance_exit
    def remove_image(self, collection_id, names):
        """
        Remove images from a collection.

        Args:
            collection_id (str): Collection ID.
            names (str or sequence of strs): List of image names to be removed.

        Returns:
            If errors do occur then the data that caused the errors will be
            returned.

        """
        # Force iterable
        if not isinstance(names, (list, tuple)):
            names = [names]
        n_names = len(names)

        # Get number of threads
        num_threads = min(self.max_threads, n_names)

        # Process urls.
        if num_threads > 1:
            with closing(ThreadPool(num_threads)) as thread_pool:
                results = thread_pool.map(self.__remove_image_worker,
                                          zip(repeat(collection_id), names))
        else:
            results = [self.__remove_image_worker((collection_id, names[0]))]

        # Extract failures.
        failures = [y for x, y in zip(results, names) if x == -1]

        # Determine how many were successful
        n_successful = n_names - len(failures)
        message = 'removeImage({} out of {} successful)'.format(n_successful, n_names)

        if n_successful == 0:
            self.logger.error(message)
            return -1
        elif n_successful < n_names:
            self.logger.warning(message)
        else:
            self.logger.info(message)

        return failures

    def __remove_image_worker(self, args):
        coll_id, img_name = args

        query_str = '{}/{}/{}/images/{}'.format(self.base_api_url,
                                                self.core_api,
                                                coll_id,
                                                img_name)

        try:
            self.request_manager.delete(query_str)
        except Exception:
            return -1

    @logging_utils.log_entrance_exit
    def copy(self, collection_id, new_name):
        """
        Copy a collection and its contents to a new collection.

        Args:
            collection_id (str): Collection ID.
            new_name (str): New collection name.

        Returns:
            str: New collection ID.

        """
        # Get the collection metadata that needs to be copied.
        query_str = '{}/{}/{}'.format(self.base_api_url,
                                      self.core_api,
                                      collection_id)
        resp_json = self.request_manager.get(query_str).json()

        # Get the images that exist in the collection.
        image_names = self.images(collection_id)['images']

        # Add images to new collection.
        data = [{'collection_id': collection_id, 'image': x} for x in image_names]

        # Create new collection.
        output = self.create(new_name, resp_json['description'], resp_json['tags'])
        new_id = output['collection_id']

        # Add images to new collection.
        _ = self.add_image(new_id, data)

        return new_id
