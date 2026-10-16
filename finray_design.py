import cadquery as cq
import math
import numpy as np

# 将角度的默认单位设置为度数
np.set_printoptions(precision=3, suppress=True, formatter={'all': lambda x: f'{x}°'})

def load_para():
    pass
    return

trgx = [[121.62659118  ,29.37528822  ,18.60952714  ,25.84120482,   2.87294903,
    2.7746324   , 2.7919462   , 5   ,     -19.90410564],

[121.62659118  ,29.37528822  ,18.60952714  ,25.84120482,   2.87294903,
    2.7746324   , 2.7919462   , 5   ,     -19.90410564],
    
        [121.62659118  ,40.37528822  ,20.60952714  ,25.84120482,   2.87294903,
            2.7746324   , 2.7919462   , 5   ,     -19.90410564]]


l_w = trgx[1][1]
l_h = trgx[1][0]
l_tip=trgx[1][3]
l_hh=l_h-l_tip
l_t=trgx[1][2]
t_back = trgx[1][4]
t_flex = trgx[1][5]
t_rib = trgx[1][6]
n= trgx[1][7]
d_agl = trgx[1][8]
theta_rib =30

theta = math.degrees(math.atan2(l_h, l_w/2))
theta_l = 90 - theta
a = np.sin(np.deg2rad(theta))

b=np.cos(np.deg2rad(theta_rib))
c=np.sin(np.deg2rad(theta_rib))
l_gap=(l_hh/b-n*t_rib)/(n+1)

l_base = l_w*np.tan(np.deg2rad(theta_l))
# Create a new CadQuery Workplane object
result = cq.Workplane("XY")

# Define the vertices of the triangle
p1 = cq.Vector(l_w/2, 0, 0)
p2 = cq.Vector(-l_w/2,0, 0)
p3 = cq.Vector(0, l_h, 0)
p4 = cq.Vector(l_w/2-t_flex/a, 0, 0)
p5 = cq.Vector(l_w/2-t_flex/a-(l_h-l_tip)/(l_h/l_w*2), l_h-l_tip, 0)
p6 = cq.Vector(-(l_w/2-t_back/a-(l_h-l_tip)/(l_h/l_w*2)), l_h-l_tip, 0)
p7 = cq.Vector(-(l_w/2-t_back/a), 0, 0)
# step1: Create the triangle and extrude 
sketch1 = (
    result
    .moveTo(p1.x, p1.y)
    .lineTo(p2.x, p2.y)
    .lineTo(p3.x, p3.y)
    .close()
    )

triangle1 = sketch1.extrude(l_t).edges(">Y").fillet(2.5)

#step 2 : extrude cut
#print(theta,p4,p5,p6,p7,a)
sketch2= (
    result
    .moveTo(p4.x, p4.y)
    .lineTo(p5.x, p5.y)
    .lineTo(p6.x, p6.y)
    .lineTo(p7.x, p7.y)
    .close()
    )

triangle2 = sketch2.extrude(l_t)
triangle3 = triangle1.cut(triangle2)

face = triangle3.faces("|Z")
    

#step3 add bottom
p8= cq.Vector(-l_w/2,-8, 0)
p9 = cq.Vector(l_w/2, -8, 0)

#rec = result.moveTo(p1.x, p1.y).lineTo(p2.x, p2.y).lineTo(p8.x, p8.y).lineTo(p9.x, p9.y).close().extrude(l_t).edges("<Y").fillet(2.5)
rec = result.moveTo(p1.x, p1.y).lineTo(p2.x, p2.y).lineTo(p8.x, p8.y).lineTo(p9.x, p9.y).close().extrude(l_t).edges("<Y")

#cut cavity for base
p10 = cq.Vector(-13, -2,0)
p11=cq.Vector(-13, -5.2,0)
p12=cq.Vector(-8, -5.2, 0)
p13=cq.Vector(-8,-8,0)
p14=cq.Vector(8,-8,0)
p15=cq.Vector(8, -5.2,0)
p16=cq.Vector(13, -5.2, 0)
p17=cq.Vector(13, -2,0)

cavity = result.moveTo(p10.x, p10.y).lineTo(p11.x, p11.y).lineTo(p12.x, p12.y).lineTo(p13.x, p13.y).lineTo(p14.x, p14.y) \
                    .lineTo(p15.x, p15.y).lineTo(p16.x, p16.y).lineTo(p17.x, p17.y).close().extrude(l_t) 

                        
rec1 = rec.cut(cavity)

fin = triangle3.add(rec1)

p18=cq.Vector(-l_w/2, -8,0)
p19=cq.Vector(l_w/2, -8,0)
p20=cq.Vector(l_w/2, -8-l_base ,0)

#add basic base part   triangle part to adjust angle
cavity2 = result.moveTo(p18.x, p18.y).lineTo(p19.x, p19.y).lineTo(p20.x, p20.y).close().extrude(l_t)

p199=cq.Vector(l_w/2+(l_w/np.cos(np.deg2rad(theta_l))-l_w), -8,0)
p21 =  cq.Vector(l_w/2, -18,0)
p22 =  cq.Vector(l_w/2-8, -26,0)
p23 =  cq.Vector(-l_w/2+8, -26,0)
p24 =  cq.Vector(-l_w/2, -18,0)
#.edges("|Z").fillet(2)

holes = [(10, -18), (-10, -18)]

#### add  basic part 
cavity3 = result.moveTo(p18.x, p18.y).lineTo(p199.x, p199.y).lineTo(p20.x, p20.y).lineTo(p21.x, p21.y).lineTo(p22.x, p22.y).lineTo(p23.x, p23.y).lineTo(p24.x, p24.y).close() \
                    .extrude(l_t) \
                     .faces(">Z").workplane().pushPoints([(-10, -18), (10, -18)]) \
                     .circle(1.6).cutThruAll()
                     
                     
# Define a text string and add it to the model
text_string = "Basic"
texts = cq.Workplane().text(text_string, 6, 5)

#show_object() 
#define the part that needs to be cut from the basic part 
cavity4 = cq.Workplane("XY").transformed(offset=(0, 0, l_t/2-7.5)).moveTo(p18.x, p18.y-4).lineTo(p199.x, p199.y-5).lineTo(p20.x, p20.y).lineTo(p21.x, p21.y) \
                    .lineTo(p22.x, p22.y) \
                    .lineTo(p23.x, p23.y).lineTo(p24.x, p24.y).close() \
                    .extrude(15)

#cur the part and rotate 
#cavity3 = cavity3.cut(cavity4).faces("<Y").fillet(0.5) \
cavity5 = cavity3.cut(cavity4)\
                .rotate((-l_w/2, -8,0), (-l_w/2, -8,l_t), angleDegrees=-(90-theta))

cavity6 = cavity5.add(cavity).add(cavity2)


#add ribs
for i in range (1, n+1):
    pp1 = cq.Vector(0,l_gap*i+(i-1)*t_rib,0)
    pp2 = cq.Vector(0,l_gap*i+i*t_rib,0)
    pp3 = cq.Vector(0,l_gap*i+i*t_rib,l_t)
    pp4 = cq.Vector(0,l_gap*i+(i-1)*t_rib,l_t)
    
    dis_x = (pp1.y+pp2.y)/2*c
    dis_y = (pp1.x+pp2.x)/2*c
#    print('debug', dis)
    #part = cq.Workplane("YZ")
    sketchh = 'sketch'
    sketch = sketchh + str(i)

    sketch_trans = (
        fin
        .faces(">X")
        .workplane()
#        .transformed((0, 0, 0), (0,0,-l_w/2))
        .transformed((0, 0, 0), (0,0,-(l_w/2)+dis_x))
        .transformed((0, theta_rib, 0), (0,0,0))
        
        .moveTo(pp1.y, pp1.z)
        .lineTo(pp2.y, pp2.z)
        .lineTo(pp3.y, pp3.z)
        .lineTo(pp4.y, pp4.z)
        .close()
        )
    #transform sketch

 #   fin.plane.zDir = cq.Vector(0,1,1).normalized()

#    rib = sketch_trans.extrude("next",  both=True)
    rib = sketch_trans.extrude("next", both=True)
    fin= fin.add(rib)
    n+=1

    #rib = sketch3.extrude("next", both=True)
fin= fin.rotate((0,0,0), (0,1,0), angleDegrees=90).rotate((0,0,0), (1,0,0), angleDegrees=10).translate((-l_t/2,0,0))



cq.exporters.export(fin, "/home/wan383/projects/sofa-sim/clone/finray-pinch/data/finray_2.step")

#add base 
sketch5= (
    result
    .moveTo(p4.x, p4.y)
    .lineTo(p5.x, p5.y)
    .lineTo(p6.x, p6.y)
    .lineTo(p7.x, p7.y)
    .close()
    )

base = cavity6.rotate((0,0,0), (0,1,0), angleDegrees=90).rotate((0,0,0), (1,0,0), angleDegrees=10).translate((-l_t/2,0,0))
fin_whole = fin.add(base)


show_object(fin)

cq.exporters.export(fin, "/home/wan383/projects/sofa-sim/clone/finray-pinch/data/print.step")