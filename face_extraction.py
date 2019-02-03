def get_face_poses_from_tags(image, tags):
    img_width, img_height = image.size

    faces = []
    for name, x, y, width, height in tags:
        center_x = x*img_width
        center_y = y*img_height

        total_width = width*img_width
        total_height = height*img_height

        half_width = total_width/2.0
        half_height = total_height/2.0

        top = center_y-half_height
        bottom = center_y+half_height
        left= center_x-half_width
        right = center_x+half_width

        face = {"name": name, "top": top, "bottom": bottom, "left": left, "right": right}
        faces.append(face)
    return faces
