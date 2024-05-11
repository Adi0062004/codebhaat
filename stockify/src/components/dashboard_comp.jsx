

import React from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { useDrag } from 'react-dnd'
import { ItemTypes } from './Constants'



export default function Card({ isDragging, text }) {
    const text="hello there";
    const [{ opacity }, dragRef] = useDrag(
        () => ({
      type: ItemTypes.CARD,
      item: { text },
      collect: (monitor) => ({
        opacity: monitor.isDragging() ? 0.5 : 1
      })
    }),
    []
  )
  return (
    <Card ref={dragRef} style={{ opacity , width: '18rem'}}>
        <Card.Img variant="top" src="holder.js/100px180"/>
        <Card.Body>
        <Card.Title>Widget</Card.Title>
        <Card.Text>
        {text}
        </Card.Text>
        <Button variant="primary">Button</Button>
      </Card.Body>
        
      
    </Card  >
  )
}