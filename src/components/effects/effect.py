class Effect:
    animation_list = []
    
    @staticmethod
    def draw(SCREEN):
        for i in Effect.animation_list:
            SCREEN.blit(i.image, i.pos)
    
    @staticmethod
    def update():
        list=[]
        for i in range(len(Effect.animation_list)):
            Effect.animation_list[i].animation_tick-=1
            if(Effect.animation_list[i].animation_tick==0):
                Effect.animation_list[i].animation_frame+=1
                if(Effect.animation_list[i].animation_frame==len(Effect.animation_list[i].image_list)):
                    list.append(i)
                    continue
                Effect.animation_list[i].image=Effect.animation_list[i].image_list[Effect.animation_list[i].animation_frame][0]
                Effect.animation_list[i].animation_tick=Effect.animation_list[i].image_list[Effect.animation_list[i].animation_frame][1]

        list.reverse()
        for i in list:
            del Effect.animation_list[i]
        