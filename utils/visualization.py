
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

def create_radar_chart(section_data: Dict[str, Any], title: str = "Section Performance") -> go.Figure:
    """
    Creates a radar chart from section performance data.
    
    Args:
        section_data: Dictionary where keys are section names and values 
                     are dictionaries containing 'correct' and 'total', or just raw scores.
                     Example: {'Reading': {'correct': 8, 'total': 10}, ...}
    
    Returns:
        Plotly Figure object
    """
    categories = []
    values = []
    
    for section, data in section_data.items():
        categories.append(section)
        # Calculate percentage
        if isinstance(data, dict) and 'total' in data and data['total'] > 0:
            percentage = (data.get('correct', 0) / data.get('total', 1)) * 100
        elif isinstance(data, (int, float)):
             percentage = data # Assume pre-calculated percentage
        else:
            percentage = 0
        values.append(percentage)
    
    # Close the loop for radar chart
    if categories:
        categories.append(categories[0])
        values.append(values[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Score',
        line_color='#3B82F6',
        fillcolor='rgba(59, 130, 246, 0.2)',
        hoverinfo='skip'  # 호버 정보 비활성화
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='#E5E7EB'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#1F2937'),
                linecolor='#E5E7EB'
            ),
            bgcolor='white'
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
        title=dict(
            text=title,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=14)
        )
    )

    return fig
