import cadquery as cq
import math

#fin = cq.Assembly()

l_w = 30
l_h = 120
l_tip= 30
l_hh=l_h-l_tip
l_t=30
t_back = 1
t_flex = 1
t_rib = 3
n= 2
l_gap=20
d_agl = 30

theta = math.degrees(math.atan2(l_h, l_w/2))

a = (math.sin(theta))
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
triangle1 = result.moveTo(p1.x, p1.y).lineTo(p2.x, p2.y).lineTo(p3.x, p3.y).close().extrude(l_t)

#step 2 : extrude cut
#print(theta,p4,p5,p6,p7,a)
triangle2=  result.moveTo(p4.x, p4.y).lineTo(p5.x, p5.y).lineTo(p6.x, p6.y).lineTo(p7.x, p7.y).close().extrude(l_t)

triangle3 = triangle1.cut(triangle2)
#step3 add botto,
p8= cq.Vector(-l_w/2,-8, 0)
p9 = cq.Vector(l_w/2, -8, 0)

rec = result.moveTo(p1.x, p1.y).lineTo(p2.x, p2.y).lineTo(p8.x, p8.y).lineTo(p9.x, p9.y).close().extrude(l_t)

#cut cavity for base
p10 = cq.Vector(-13, -2,0)
p11=cq.Vector(-13, -5.2,0)
p12=cq.Vector(-8, -5.2, 0)
p13=cq.Vector(-8,-8,0)
p14=cq.Vector(8,-8,0)
p15=cq.Vector(8, -5.2,0)
p16=cq.Vector(13, -5.2, 0)
p17=cq.Vector(13, -2,0)

cavity = result.moveTo(p10.x, p10.y).lineTo(p11.x, p11.y).lineTo(p12.x, p12.y).lineTo(p13.x, p13.y).lineTo(p14.x, p14.y).lineTo(p15.x, p15.y).lineTo(p16.x, p16.y).lineTo(p17.x, p17.y).close().extrude(l_t)
rec1 = rec.cut(cavity)
fin = triangle3.add(rec1)

#add ribs
pp1 = cq.Vector(0,l_gap,0)
pp2 = cq.Vector(0,l_gap+t_rib,0)
pp3 = cq.Vector(0,l_gap+t_rib,l_t)
pp4 = cq.Vector(0,l_gap,l_t)

part = cq.Workplane("YZ")

#rib = part.moveTo(pp1.x, pp1.y).lineTo(pp2.x, pp2.y).lineTo(pp3.x, pp3.y).lineTo(pp4.x, pp4.y).close().extrude(10)

rib = part.moveTo(pp1.y, pp1.z).lineTo(pp2.y, pp2.z).lineTo(pp3.y, pp3.z).lineTo(pp4.y, pp4.z).close().extrude(20)


fin= fin.add(rib)

show_object(fin)
