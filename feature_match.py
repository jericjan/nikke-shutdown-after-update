# https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html

import cv2 as cv

# import matplotlib.pyplot as plt


def find_match(path):
    img1 = cv.imread("login_screen.png", cv.IMREAD_GRAYSCALE)  # queryImage
    img2 = cv.imread(path, cv.IMREAD_GRAYSCALE)  # trainImage
    # Initiate SIFT detector
    sift = cv.SIFT_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    # draw_params = dict(
    #     matchColor=(0, 255, 0),
    #     singlePointColor=(255, 0, 0),
    #     matchesMask=matchesMask,
    #     flags=cv.DrawMatchesFlags_DEFAULT,
    # )
    # img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
    # plt.imshow(img3,),plt.show()
    actual_matches = len([x for x in matchesMask if x != [0, 0]])
    print(
        f"{actual_matches} matches out of {len(matchesMask)} ({actual_matches/len(matchesMask)*100:.2f}%)"
    )
    if actual_matches >= 100:
        return True
    return False
