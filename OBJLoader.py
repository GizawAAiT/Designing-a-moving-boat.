import numpy as np


class ObjFileLoader:
    buffer = []

    def search_data(data_values, container, identifier, data_type): #identifier includes [v, vt, f...]
        for d in data_values:
            if d == identifier:
                continue
            if data_type == 'float':
                container.append(float(d))
            elif data_type == 'int':        
                container.append(int(d)-1)


    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                ObjFileLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1: # sort the texture coordinates
                start = ind * 2
                end = start + 2
                ObjFileLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2: # sort the normal vectors
                start = ind * 3
                end = start + 3
                ObjFileLoader.buffer.extend(normals[start:end])


    def create_unsorted_vertex_buffer(indices_data, vertices, textures, normals):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            start = i1 * 3
            end = start + 3
            ObjFileLoader.buffer.extend(vertices[start:end])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    start = indices_data[i2 + 1] * 2
                    end = start + 2
                    ObjFileLoader.buffer.extend(textures[start:end])

                    start = indices_data[i2 + 2] * 3
                    end = start + 3
                    ObjFileLoader.buffer.extend(normals[start:end])

                    break


    def show_buffer_data(buffer):
        for i in range(len(buffer)//8):
            start = i * 8
            end = start + 8
            print(buffer[start:end])


    def load_model(file, sorted=True):
        
        """define all the list container for vertices, textures, normals, indices .."""
        
        vertices = [] # all vertex coordinates
        textures = [] #  all texture coordinates
        normals = [] #all vertex normals.

        all_indices = [] # will contain all the vertex, texture and normal indices
        indices = [] # will contain the indices for indexed drawing


        with open(file, 'r') as fl:
            line = fl.readline()
            while line:
                line_data = line.split(' ')
                if line_data[0] == 'v':
                    ObjFileLoader.search_data(line_data, vertices, 'v', 'float')
                elif line_data[0] == 'vt':
                    ObjFileLoader.search_data(line_data, textures, 'vt', 'float')
                elif line_data[0] == 'vn':
                    ObjFileLoader.search_data(line_data, normals, 'vn', 'float')
                elif line_data[0] == 'f':
                    for value in line_data[1:]:
                        val = value.split('/')
                        ObjFileLoader.search_data(val, all_indices, 'f', 'int')
                        indices.append(int(val[0])-1)

                line = fl.readline()

        if sorted:
            # use with glDrawArrays
            ObjFileLoader.create_sorted_vertex_buffer(all_indices, vertices, textures, normals)
        else:
            # use with glDrawElements
            ObjFileLoader.create_unsorted_vertex_buffer(all_indices, vertices, textures, normals)

        # ObjLoader.show_buffer_data(ObjLoader.buffer)

        local_copy = ObjFileLoader.buffer.copy() # create a local copy of the buffer list, otherwise it will overwrite the static field buffer
        ObjFileLoader.buffer = [] # after copy, make sure to set it back to an empty list

        return np.array(indices, dtype='uint32'), np.array(local_copy, dtype='float32')

