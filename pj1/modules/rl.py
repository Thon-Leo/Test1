# import numpy as np

# time_passed = 0.017
# half_gap = 75
# policy = dict()
# """
# Given the current x, y, z, will the bird collide?

# inputs: x: pipe x - bird x, range(0,150)
#         y: center of gap - center of bird   range(-150, 150)
#         z: bird speed   range(-15.0,15.0)

#         bird y: 0 top, 380 ground
#         pipe height: 320 
#         bird width: 34
#         pipe width: 52
# """
# def will_colide(x: int, y: int, z: float):
#     # every jump can raise about 30 pixels, 8 frames
    
#     # inevitable collides
#     if x < 66 and (y < -(half_gap+34) or y > (half_gap+34)):
#         return True
#     else:
#         # see if we will collide during moving up
#         while z > 0:
#             # inevitable collides
#             if x < 66 and (y < -(half_gap+34) or y > (half_gap+34)):
#                 return True
#             # hits the top pipe
#             if x < 17 and (y < -(half_gap-34) or y > (half_gap-34)):
#                 return True
        
#             # update and see if next frame will collide
#             x -= 4
#             z -= 60 * time_passed
#             y -= z


#     return False

# """
# Given the current x, y, z, what is the best action?

# inputs: x: pipe x - bird x, range(0,150)
#         y: center of gap - center of bird   range(-150, 150)
#         z: bird speed   range(-15.0,15.0)

#         bird y: 0 top 380 ground
#         pipe height: 320 
# """ 
# def best_act(x, y, z):
    
#     flap_speed = max(z+1, 12)
#     # if flap will collide?
#     flap_speed -= 60 * time_passed
#     flap_height -= flap_speed
#     flap_b = will_colide(x-4, flap_height, flap_speed) # next frame

#     # if idle will collide?
#     idle_speed = z - 60*time_passed
#     idle_height -= idle_speed
#     idle_b = will_colide(x-4, idle_height, idle_speed) # next frame

#     flap_value = -1000 * flap_b - abs(flap_height)
#     idle_value = -1000 * idle_b - abs(idle_height)

#     if flap_value > idle_value:
#         return True
#     return False


# def flap(bird, pipe_sprites):
#     # distance
#     pipe_top = pipe_sprites.sprites()[0]
#     distance = pipe_top.rect.left - bird.rect.left

#     if distance < 0:
#         pipe_top = pipe_sprites.sprites()[2]
#         distance = pipe_top.rect.left - bird.rect.left
#     distance = min(distance, 149)
    
#     # height
#     if distance >= 149:
#         height = 190 - bird.rect.centery
#     else:
#         height = pipe_top.rect.bottom + half_gap - bird.rect.centery
#     if height < -149:
#         height = -149
#     elif height > 149:
#         height = 149

#     # speed
#     speed = round(bird.up_speed, 1) if bird.is_is_flapped else -round(bird.down_speed, 1)
#     # speed = round(bird.speed, 1)

#     if speed > 15:
#         speed = 15.0
#     elif speed < -15:
#         speed = -15.0
    


#     return policy[distance][height][speed]

# for x in range(0, 150):
#     for y in range(-150, 151):
#         for z in range(-150, 151):
#             policy[(x, y, z / 10)] = best_act(x, y, z / 10)