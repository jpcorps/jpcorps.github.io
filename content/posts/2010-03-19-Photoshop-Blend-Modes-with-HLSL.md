---
title: "Photoshop Blend Modes with HLSL"
date: 2010-03-19T11:09:48Z
draft: false
---

<http://blog.naver.com/frustum?Redirect=Log&logNo=150042116101>  
  
Photoshop Blend Modes with HLSL  
  
  
Kyle Schouviller  
  
  
Photoshop and other image editing programs offer artists a lot of power with layer blending modes. These allow an artist to perform a color operation when one layer is blended on top of another. For example, multiply will make the bottom layer darker based on the top layer, and is great for blending color fills on top of line art (the lines stay black while the inside gets filled).  
Many of these effects can be achieved using the blending operations available in HLSL. Better yet, you barely need to know any HLSL to create them ? some don’t even require a special shader to work.??  

Prerequisites
-------------

For this tutorial, all you’ll need is a little bit of experience with basic algebra. You need to understand how to rearrange one side of an equation. You’ll also need XNA Game Studio 3.0 to compile and run the sample, and to create your own effects.

Intoduction to Blending
-----------------------

One of the first places you’ll probably encounter blending operations is when you’re trying to make alpha blending work. Usually you’ll have a sprite with some transparency, and you want it to have the same transparency when you draw it in XNA. When you look it up online, you’ll find something like this:

SourceBlend = SourceAlpha

DestinationBlend = InverseSourceAlpha

Blend = Add

You stick the code in your application and alpha blending magically works! But what’s really happening?

The Blending Equation
---------------------

When you draw a picture on the screen, a lot happens. What it all boils down to though is determining what color to put in what pixel, based on what you want to draw, and what’s already there.

For example, let’s say you wanted to draw the edge of a red ball on top of a blue background. The edge of the ball is a little bit transparent though, to make it have softer edges. When you draw that partially transparent red edge on top of the blue, what happens? Does that pixel stay blue? Does it turn red? Do the two colors get blended?

Pixels are combined based on the blending settings you set. There are five components that determine how colors are blended:

·         Source Color: The color that you are writing to the pixel.

·         Destination Color: The color that is already in that pixel.

·         BlendOperation: This is how the colors will be combined.

·         SourceBlend: This specifies what the source color will be multiplied by before the blend operation occurs. For example, SourceAlpha will multiply the source color by its alpha.

·         DestinationBlend: This specifies what the destination color will be multiplied by before blending.

When you draw something, the value that comes out of your pixel shader is the source color (usually just the texture you’re drawing). What’s already on the screen is the destination color (the background). These colors first get multiplied by the Source and Destination Blend factors, respectively. Then they are combined using the blend operation you specified.

In other words, the resulting pixel value is:

Result = source \* (SourceBlend) (BlendOperation) destination \* (DestinationBlend)

For example, if we were to draw a slightly-transparent red on top of a blue background, and we wanted to do basic alpha blending, we’d have the following states set:

Source color: slightly-transparent red (1,0,0,0.75)

Destination color: full blue (0,0,1,1)

Blend Mode: Add

SourceBlend: SourceAlpha

DestinationBlend: InverseSourceAlpha

So first, we’re going to multiply the source and destination by their blend factors:

Source = source \* SourceAlpha = (1, 0, 0) \* 0.75 = (0.75, 0, 0)

Destination = destination \* InverseSourceAlpha = (0, 0, 1) \* (1 – 0.75) = (0, 0, 0.25)

Then, we’re going to perform the blend operation on the resulting colors, which in this case is addition:

Result = Source + Destination

Result = (0.75, 0, 0) + (0, 0, 0.25)

Result = (0.75, 0, 0.25)

We’ve created a pixel that is 75% red and 25% blue. This is how alpha blending works.

Simple Effects
--------------

It turns out there are quite a few effects that are done entirely with blend modes. These are the Photoshop modes Darken, Lighten, Linear Dodge and Multiply. We’ll look at the equations for each of these, and then how we can make them using blend modes.

### Linear Dodge

![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image001.jpg)

Linear Dodge is a blending mode that brightens the bottom layer by adding the top layer. In other words:

Result = source + destination

So, how can we do this with blend modes? Well, we want the operation to be add since we want to add the colors together. Because we aren’t changing the colors before adding them, we’re just going to use a blend factor of one for each of them. This will multiply them by 1, leaving them as they are.

BlendOperation = Add

SourceBlend = One

DestinationBlend = One

That’s all there is to it! This can be done really easily with a few lines of C# in an XNA program, or can be done directly in an HLSL shader (we’ll discuss programming these later).

### Darken and Lighten

![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image002.jpg)![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image003.jpg)

Darken works by using the lowest value from the source and destination colors, and lighten uses the highest value. In other words:

Darken: result = min( source, destination )

Lighten: result = max( source, destination )

This is very similar to Linear Dodge – we don’t need to change the source or destination colors, so we’ll leave the blend factors as one. However, we need different blend operations for the effects. Luckily, min and max are both blend operations we can use.

Darken:

BlendOperation = Min

SourceBlend = One

DestinationBlend = One

Lighten:

BlendOperation = Max

SourceBlend = One

DestinationBlend = One

### Multiply

![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image004.jpg)

Multiply is an interesting blend mode. It darkens colors by multiplying them together. It’s great for blending colors on top of line art – the line art will have white (1) and black (0) areas, and when the color is multiplied on top of the line art, the white areas become the color, and the black areas will stay black. The equation is:

Result = source \* destination

There isn’t a Multiply Blend Operation, so we have to somehow multiply the source color by the destination color. Unfortunately, we don’t have access to the destination color directly – all we can use are the source color, the blend operation and the blend factors.

However, we know that multiplication happens. Before the blend operation occurs, the source and destination colors are multiplied by their blend factors. It just so happens that there are blend factors for each of the colors – in other words, we can access a color through the blend factor.

So, if we set the SourceBlend to the DestinationColor, we end up with:

Result = (source \* SourceBlend) + (destination \* DestinationBlend)

Result = (source \* destination) + (destination \* DestinationBlend)

This gives us what we want in the first half of our equation. So we can just set the DestinationBlend to Zero to eliminate the second half of the equation:

Result = (source \* destination) + (destination \* 0)

Result = (source \* destination)

So we end up with this:

BlendOperation = Add

SourceBlend = DestinationColor

DestinationBlend = Zero

Rules for Blending
------------------

There are a few rules when working with blending:

·         The variables you can manipulate are the Source color, BlendOperation, SourceBlend and DestinationBlend.

·         The source color is always multiplied by the SourceBlend, and the destination color is always multiplied by the DestinationBlend.

·         The destination color is not readable. You may place it in an equation by manipulating the blending variables, but you may not directly access it.

·         The source color will be clamped to the range [0,1] before any of the blending happens (assuming you use the default surface format).

·         Blending works on each color channel individually. So max( (0,1,0), (1,0,0) ) will result in (1,1,0).

Manipulating the Source Color
-----------------------------

For more complicated effects, we need to manipulate the source color before it reaches the blending equation. This allows us greater control over how the blending equation works.

### Multiply

For example, we could have done the multiply operation a different way. Instead of using Zero as one of the blend factors, we could have multiplied both colors by each other. This would have given us twice the value we wanted, since it would have multiplied the source and destination values twice and added them together:

BlendMode = Add

SourceBlend = DestinationColor

DestinationBlend = SourceColor

In other words, we end up with:

Result = (source \* destination) + (destination \* source)

So what we need to do is divide by two. However, we can’t do this in the blending equation directly – we have to manipulate the source color. If we multiply the source color by 0.5 (dividing it by two), we end up with this:

Result = ((source \* 0.5) \* destination) + (destination \* (source \* 0.5))

Result = 2 \* (0.5 \* source \* destination)

Result = 2 \* 0.5 \* source \* destination

Result = source \* destination

It’s the same result as we had earlier, but we obtained it by manipulating the source color.

### Linear Burn

![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image005.jpg)

Linear Burn looks like an easy effect. The equation is:

Result = source + destination – 1

You might think to rearrange the equation like this so it’s a simple addition problem:

Result = (source – 1) + destination

If you do this, you’re always going to end up with the destination color. Why?

Assume that both the source and destination colors are half-gray (0.5, 0.5, 0.5) – which I’ll just write as 0.5. If we use the original equation, we end up with:

Result = 0.5 + 0.5 – 1 = 1 – 1 = 0

Or black. If we use our new equation, we find a problem:

Result = (0.5 – 1) + 0.5

Result = (-0.5) + 0.5

Result = 0 + 0.5

Result = 0.5

Why did the 0.5 value change to 0? The fourth rule says that colors are clamped to the range [0,1] before the blending operation occurs. This means that if the source color is less than 0, it will always be rounded up to 0 before the rest of the blending happens – which will always happen if we subtract one from our source color (colors are always in the range of 0 to 1 for a default surface type).

So we need to rearrange the original equation so the source color is never less than 0:

Result = source + destination – 1

Result = destination + source – 1

Result = destination – (1 – source)

Subtracting the source color from one will always result in a number between 0 and 1 (since the source color is always in the range [0,1]), and the destination color is left as its original value. Additionally, there’s a blend mode that allows us to subtract the source color from the destination color – RevSubtract. So our final result will be:

Source = 1 – source

BlendOperation = RevSubtract

SourceBlend = One

DestinationBlend = One

### Screen

![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image006.jpg)

Even trickier is the Screen effect. The original equation is quite imposing:

Result = 1 – (1 – destination) \* (1 – source)

If it weren’t for the one in the front, this would be rather straightforward. However, there’s a way to rearrange the algebra to get it in a form that makes blending easy.

First, expand the equation:

Result = 1 – (1 – source – destination + destination \* source)

Next, eliminate the ones

Result = 1 – 1 + source + destination – destination \* source

Result = source + destination – destination \* source

All we half left is to rearrange this into the form of the blending equation, where source is multiplied by something and destination is multiplied by something. The InvDestColor blend mode lets us multiply by (1 – destination), which we can obtain by rearranging the equation as follows:

Result = destination + source – source \* destination

Result = destination + source \* (1 – destination)

Now that we have the math worked out, we simply have to set the blend modes

BlendOperation = Add

DestinationBlend = One

SourceBlend = InvDestColor

Putting it All Together – Hard Light
------------------------------------

![](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes//image007.jpg)

Now that we have multiply and screen figured out, we can do the Hard Light effect, which is a combination of the two. Hard light will multiply colors if the source is less than or equal to 0.5, and will screen otherwise. The effect takes two passes – the multiply and screen pass. Each pass must perform its operation on the correct pixels, and leave the others alone. For example, with a source of 0.25 on the screen pass, the destination color must be left alone.

### The Multiply Pass

For the multiply pass, we want to only use the source color when it’s between 0 and 0.5. We then multiply it by two to obtain a value between 0 and 1, which we use for the multiply operation.

It’s easy to do this using the second method we came up with for multiply above. In that method, we divided the source color by 2 and then multiplied it by the destination color twice and added the results together, ending with source \* destination. For this pass, since we’ll need to multiply by two beforehand anyways, we can just cut out the two from the equation altogether. In other words, in the original, we had:

Source = source / 2

In this one, we want

Source = source \* 2

So if we use the method we came up with above, we have:

Source = source \* 2 / 2 = source

BlendMode = Add

SourceBlend = DestinationColor

DestinationBlend = SourceColor

So what we end up with is:

Result = (source \* destination) + (destination \* source)

Result = 2 \* (source \* destination)

But, since the original source color is always between 0 and 0.5, we’ll always end up with a source color between 0 and 1 (i.e. 2 \* source is always less than or equal to 1).

But how do we avoid the pixels for the screen pass? When the source color is greater than 0.5, we want to leave the destination color alone. Luckily, the math works out: when the source color is 0.5, we end up multiplying the destination color by 2 \* 0.5, or one, leaving the destination color unchanged. So we can just clamp the source color to a maximum of 0.5.

Source = min(source, 0.5)

BlendMode = Add

SourceBlend = DestinationColor

DestinationBlend = SourceColor

### The Screen Pass

The screen pass will follow a similar method. When we screen, we want to leave the destination color alone whenever the source color is less than or equal to 0.5. Luckily, this is easy. The screen equation, as derived above, is:

Result = destination + source \* (1 – destination)

So what we want to do is make the source color 0 whenever the original source color is less than or equal to 0.5, and stretch the source color between 0 and 1 otherwise (since the original values will be between 0.5 and 1). We can do this by subtracting 0.5 from the source color, multiplying the result by two, and then clamping the minimum to 0. Then, when our source color is less than or equal to 0.5, it will end up as 0, which will leave the destination color as the result:

Result = destination + ((0.5 – 0.5) \* 2.0) \* (1 – destination)

Result = destination + (0) \* (1 – destination)

Result = destination

So our final method is:

Source =max(((source – 0.5) \* 2.0), 0.0)

BlendMode = Add

SourceBlend = InvDestColor

DestBlend = One

Exercises
---------

These can all be solved, and are all combinations of the above effects. They should be fairly straightforward to solve – just look to how the Hard Light effect worked. The resources section contains a link to an article that contains equations for all of these effects.

### Soft Light

Similar to Hard Light, so there shouldn’t be any problems getting this set up – look for the equations in the resources section at the end of this article.

### Linear Light

This effect uses linear burn and linear dodge, both of which we’ve solved. It burns if the source is less than or equal to 0.5, and dodges otherwise.

### Pin Light

This is a combination of Darken and Lighten – darken if less than or equal to 0.5, lighten otherwise.

Difficult Modes
---------------

The following blend modes all have some sort of problem that makes them difficult to solve (the demo code has blank shaders for you to fill in to try to achieve the expected result). They each have some problem with the above rules which must be overcome somehow. Most of them could be solved using a surface type that didn’t clamp values to [0, 1], but I’ll let you see if you can solve these effects with the default surface type.

### Color Burn

Result = 1 – (1 – destination) / source

The problem is that you must divide by the source color, and then subtract the result from one. Division isn’t supported before ps2.0, and there’s no simple way to resolve the subtraction from one without a separate pass. However, a separate pass would mean the original result must be stored, which is within the range of 0 to infinity, which is clamped to the range [0,1].

### Color Dodge

Result = destination / (1 – source)

Color Dodge suffers the same problems as Color Burn. There must be a division, and the result will be clamped to [0,1]. You can’t get the destination color directly, so the clearest method is to store (1 / (1 – source)) in the source color – but it will be clamped to a max of 1.

### Overlay

This is the same effect as Hard Light, except the source and destination are switched. This creates a problem, as we can’t do any direct math on the destination color.

### Vivid Light

Uses color burn and color dodge – solve those and you should be able to solve this one.

### Difference

Result = abs( destination – source )

The only issue here is that there’s no “abs” blend mode, and you can’t store the original destination color between passes. So you have to know which value is larger before you do a subtraction. If you can figure that out, you can figure out this effect.

### Exclusion

Result = 0.5 – 2 \* (destination – 0.5) \* (source – 0.5)

This looks like screen, but the subtraction is reversed, making it more difficult to fit into the blend modes and blend factors that are available.

Conclusion
----------

Blend modes offer you a wide variety of color operations with a minimum amount of code. They also perform as well as alpha blending in most cases, and run at a very low shader spec – all of the solved blending modes in this tutorial run at or below pixel shader version 1.4. All they require you to do is work out the math!

Demo
----

[Download the Sample](http://www.ziggyware.com/ZiggywareImages/Articles/blendmodes/PhotoshopBlendModes.zip)

This application includes shaders for all blend modes, and displays the source image, destination image, and a pre-rendered expected result for all of the shaders. All of the blend modes solved in this tutorial are solved in the demo, and the ones that aren’t solved are in the demo as empty shaders – ready for you to fill in with your solutions!

Resources
---------

A thorough discussion of blend mode math in Photoshop 7. In this document, “Blend” is the source color and “Base” is the destination color: < <http://dunnbypaul.net/blends/> >

A primer for blending in XNA: < <http://msdn.microsoft.com/en-us/library/bb976070.aspx> >.

The BlendFunction enumeration, listing blend operations usable directly in XNA: < <http://msdn.microsoft.com/en-us/library/microsoft.xna.framework.graphics.blendfunction.aspx> >.

The Blend enumeration, listing SourceBlend and DestinationBlend operations usable directly in XNA: < <http://msdn.microsoft.com/en-us/library/microsoft.xna.framework.graphics.blend.aspx> >.

D3DBLENDOP – remove the “D3DBLENDOP\_” at the beginning to use these as blend operations in an HLSL shader: < <http://msdn.microsoft.com/en-us/library/bb172509(VS.85).aspx> >

D3DBLEND – remove the “D3DBLEND\_” at the beginning to use these as blend factors in an HLSL shader: < <http://msdn.microsoft.com/en-us/library/bb172508(VS.85).aspx> >