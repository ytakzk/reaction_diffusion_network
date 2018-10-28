def export_obj(mesh,filename="output.obj"):
    out = createWriter(filename)
    out.println("# mesh exported from p5py by mathias")
    
    mesh.collect_nodes()
    
    for n in mesh.nodes:
        out.println("v {} {} {}".format(n.x,n.y,n.z))
        
    out.println("g triangles")
    tris = [f for f in mesh.faces if len(f.nodes)==3]
    for f in tris:
        index_list = [str(n.id) for n in f.nodes]
        out.println("f "+" ".join(index_list))

    out.println("g quads")
    quads = [f for f in mesh.faces if len(f.nodes)==4]
    for f in quads:
        index_list = [str(n.id) for n in f.nodes]
        out.println("f "+" ".join(index_list))
        
    out.flush()
    out.close()
    
def get_pshape(mesh):
    # create pshape object
    my_pshape = createShape(GROUP)
    
    # start adding triangular faces
    tris = [f for f in mesh.faces if len(f.nodes)==3]
    my_tris = createShape()
    my_tris.beginShape(TRIANGLES)
    for f in tris:
        for n in f.nodes:
            my_tris.vertex(n.x,n.y,n.z)
    my_tris.endShape()
    my_pshape.addChild(my_tris)
    
    # start adding quad faces
    quads = [f for f in mesh.faces if len(f.nodes)==4]
    my_quads = createShape()
    my_quads.beginShape(QUADS)
    for f in quads:
        for n in f.nodes:
            my_quads.vertex(n.x,n.y,n.z)
    my_quads.endShape()
    my_pshape.addChild(my_quads)
    
    # start adding other faces
    others = [f for f in mesh.faces if len(f.nodes)>4]
    for f in others:
        face = createShape()
        face.beginShape()
        for n in f.nodes:
            face.vertex(n.x,n.y,n.z)
        face.endShape(CLOSE)
        my_pshape.addChild(face)
    
    # return 1 pshape object
    return my_pshape
