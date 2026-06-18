import os
import pygame
import random
import time
import neat
pygame.font.init()

win_width=600
win_height=800
gen=0

pygame.display.set_caption("AI FLAPPY BIRD")
icon=pygame.image.load('brothers.png')
pygame.display.set_icon(icon)

bird_images=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
pipe_images=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
base_images=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
bg_images=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

stat_font=pygame.font.SysFont("comicsans",50)

class Bird:
    IMGS=bird_images

    max_rotation=25
    
    rot_vel=20
    animation_time=5

    def __init__(self,x,y):

        self.x=x
        self.y=y
        
        self.tilt=0
        self.tick_count=0
        
        self.vel=0
        self.height=self.y
         
        self.img_count=0
        self.img=self.IMGS[0]

    def jump(self):
        # to move upward v- to move down v+ 
        self.vel=-10.5

        self.tick_count=0

        self.height=self.y

    def move(self):

        self.tick_count+=1
        # displacement
        # self.tick_count tells time , a=3
        # - upwards +downwards
        d=self.vel*self.tick_count+1.5*self.tick_count**2

        if d>=16:
            d=16
        if d<0:
           
            d-=2

        self.y=self.y+d
        if d<0 or self.y<self.height+50:
            if self.tilt<self.max_rotation:
                self.tilt=self.max_rotation
        else:
            
            if self.tilt>-90:
                self.tilt-=self.rot_vel

    def draw(self,win):
        self.img_count+=1
        
        if self.img_count<self.animation_time:
            self.img=self.IMGS[0]
        elif self.img_count<self.animation_time*2:
            self.img=self.IMGS[1]
        elif self.img_count<self.animation_time*3:
            self.img=self.IMGS[2]
        elif self.img_count<self.animation_time*4:
            self.img=self.IMGS[1]
        elif self.img_count==self.animation_time*4+1:
            self.img=self.IMGS[0]
            self.img_count=0
        if self.tilt<=-80:
        
            self.img=self.IMGS[0]
            self.img_count=self.animation_time*2
        
        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
def draw_window(win,birds,pipes,base,score,gen):
    win.blit(bg_images,(0,0))
    for pipe in pipes:
        pipe.draw(win)


    base.draw(win)

    
    for bird in birds:
        bird.draw(win)

    text=stat_font.render("Score:"+str(score),1,(255,255,255))
    win.blit(text,(win_width-10-text.get_width(),10))

    text=stat_font.render("Gen:"+str(gen),1,(255,255,255))
    win.blit(text,(10,10))
    pygame.display.update()


class Pipe:
    gap=200
    vel=5
    def __init__(self,x):
        self.x=x
        self.height=0
        
        self.gap=200
        self.top=0
        self.bottom=0
        self.pipe_top=pygame.transform.flip(pipe_images,False,True)
        self.pipe_bottom=pipe_images

        self.passed=False
        
        self.set_height()


    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.pipe_top.get_height()
        self.bottom=self.height+self.gap

    def move(self):
    
        self.x-=self.vel

    def draw(self,win):
        win.blit(self.pipe_top,(self.x,self.top))
        win.blit(self.pipe_bottom,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask=bird.get_mask()
        
        top_mask=pygame.mask.from_surface(self.pipe_top)
        bottom_mask=pygame.mask.from_surface(self.pipe_bottom)
        
        top_offset=(self.x-bird.x,self.top-round(bird.y))
        bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))
        
        b_point=bird_mask.overlap(bottom_mask,bottom_offset)
        t_point=bird_mask.overlap(top_mask,top_offset) 
        
        if t_point or b_point:
            return True

        return False
    

class Base:
    vel=5
    width=base_images.get_width()
    img=base_images

    def  __init__(self,y):
        self.y=y
        self.x2=self.width
        self.x1=0

    def move(self):
        self.x1-=self.vel
        self.x2-=self.vel

        if self.x1+self.width<0:
            self.x1=self.x2+self.width
        if self.x2+self.width<0:
            self.x2=self.x1+self.width

    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))



        



        


def main(genomes,config):
    global gen
    gen+=1
    score=0
    nets=[]
    ge=[]
    birds=[]
    # genomeid,genome object
    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness=0
        ge.append(g)
    base=Base(730)
    pipes=[Pipe(600)]
    win=pygame.display.set_mode((win_width,win_height))
    clock=pygame.time.Clock()
    run=True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                quit()

        pipe_ind=0
        if len(birds)>0:
            # paar hui ki nahi
            if len(pipes)>1 and birds[0].x>pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind=1

        else:
            run=False
            break

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness+=0.2

            output=nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].top),abs(bird.y-pipes[pipe_ind].bottom)))

            if output[0]>0.5:
                bird.jump()
        base.move()
        # removed pipes
        rem=[]
        add_pipe=False
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness-=1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                    
           
                if not pipe.passed and pipe.x<bird.x:
                    pipe.passed=True
                    add_pipe=True
            # pipe screen pe hai ya nahi
            if pipe.x + pipe.pipe_top.get_width()<0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 10
            # spawn position
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)
        for x,bird in enumerate(birds):
            # base ke neeche image chala jaye
            if bird.y + bird.img.get_height()>=730 or bird.y<0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

                
        draw_window(win,birds,pipes,base,score,gen)

    
 

def run(config_path):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p=neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)
    # population main ko dega
    winner=p.run(main,50)

if __name__=="__main__":
    local_dir=os.path.dirname(__file__)
    config_path=os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)







