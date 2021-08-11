    with open(obj_name, 'w') as f:
        # first line: write mtlib(material library)
        # f.write('# %s\n' % os.path.basename(obj_name))
        # f.write('#\n')
        # f.write('\n')
        if texture is not None:
            f.write('mtllib %s\n\n' % os.path.basename(mtl_name))
        f.write('o Head\n')
        #Head
        # write vertices
        if colors is None:
            for i in range(3931):
                f.write('v {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2]))
        else:
            for i in range(3931):
                f.write('v {} {} {} {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2], colors[i, 0], colors[i, 1], colors[i, 2]))

        # write uv coords
        if texture is None:
            for i in range(7800):
                f.write('f {} {} {}\n'.format(faces[i, 2], faces[i, 1], faces[i, 0]))
        else:
            for i in range(3962):
                f.write('vt {} {}\n'.format(uvcoords[i,0], uvcoords[i,1]))


            f.write('usemtl %s\n' % material_name_head)
            f.write('s off\n')
            uvfaces = uvfaces + 1

            # write f: ver ind/uv ind
            for i in range(7800):
                f.write('f {}/{} {}/{} {}/{}\n'.format(
                    #  faces[i, 2], uvfaces[i, 2],
                    #  faces[i, 1], uvfaces[i, 1],
                    #  faces[i, 0], uvfaces[i, 0]
                    faces[i, 0], uvfaces[i, 0],
                    faces[i, 1], uvfaces[i, 1],
                    faces[i, 2], uvfaces[i, 2]
                )
                )

        #Eyes
        f.write('o Eyes\n')

        # write vertices
        if colors is None:
            for i in range(3931,5023):
                f.write('v {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2]))
        else:
            for i in range(3931,5023):
                f.write('v {} {} {} {} {} {}\n'.format(vertices[i, 0], vertices[i, 1], vertices[i, 2], colors[i, 0],
                                                           colors[i, 1], colors[i, 2]))

        # write uv coords
        if texture is None:
            for i in range(7800,9976):
                f.write('f {} {} {}\n'.format(faces[i, 2], faces[i, 1], faces[i, 0]))
        else:
            for i in range(3962,5118):
                f.write('vt {} {}\n'.format(uvcoords[i, 0], uvcoords[i, 1]))


            f.write('usemtl %s\n' % material_name_eye)
            f.write('s off\n')

            # write f: ver ind/ uv ind
            for i in range(7800,9976):
                f.write('f {}/{} {}/{} {}/{}\n'.format(
                        #  faces[i, 2], uvfaces[i, 2],
                        #  faces[i, 1], uvfaces[i, 1],
                        #  faces[i, 0], uvfaces[i, 0]
                    faces[i, 0], uvfaces[i, 0],
                    faces[i, 1], uvfaces[i, 1],
                    faces[i, 2], uvfaces[i, 2]
                )
                )

            # write mtl
            with open(mtl_name, 'w') as f:
                f.write('newmtl %s\n' % material_name_head)
                s = 'map_Kd {}\n'.format(os.path.basename(texture_name)) # map to image
                f.write(s)

                if normal_map is not None:
                    name, _ = os.path.splitext(obj_name)
                    normal_name = f'{name}_normals.png'
                    f.write(f'disp {normal_name}\n')
                    # out_normal_map = normal_map / (np.linalg.norm(
                    #     normal_map, axis=-1, keepdims=True) + 1e-9)
                    # out_normal_map = (out_normal_map + 1) * 0.5
                    cv2.imwrite(
                        normal_name,
                        # (out_normal_map * 255).astype(np.uint8)[:, :, ::-1]
                        normal_map
                    )
                f.write('newmtl %s\n' % material_name_eye)
                f.write('Ka 1.000000 1.000000 1.000000\n')
            cv2.imwrite(texture_name, texture)
