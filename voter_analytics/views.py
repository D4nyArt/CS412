# File: views.py
# Author: Dany Arteaga Mercado (d4nyart@bu.edu), 10/30/2025
# Description: Django views for voter analytics application. Provides
# list views with filtering capabilities, detail views for individual
# voters, and data visualizations using Plotly charts.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

import plotly 
import plotly.graph_objs as go

class VoterListView(ListView):
    """Display a paginated list of voters with filtering options.
    Results are paginated at 100 voters per page."""

    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 voters per page

    def get_queryset(self):
        """Return filtered queryset of voters based on GET parameters."""

        queryset = Voter.objects.all()
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        voter_score = self.request.GET.get('voter_score')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')

        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        
        # Apply filters if provided
        if party:
            queryset = queryset.filter(party__icontains=party)

        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        if min_birth_year:
            queryset = queryset.filter(date_birth__year__gte=min_birth_year)

        if max_birth_year:
            queryset = queryset.filter(date_birth__year__lte=max_birth_year)
        
        if v20state:
            queryset = queryset.filter(v20state=(v20state == 'true'))
        
        if v21town:
            queryset = queryset.filter(v21town=(v21town == 'true'))
        
        if v21primary:
            queryset = queryset.filter(v21primary=(v21primary == 'true'))
        
        if v22general:
            queryset = queryset.filter(v22general=(v22general == 'true'))
        
        if v23town:
            queryset = queryset.filter(v23town=(v23town == 'true'))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add filter options and voter count to template context. 
        Preserves currently selected filter values for form persistence."""

        context = super().get_context_data(**kwargs)
        context['voter_count'] = self.get_queryset().count()
        
        # Get distinct values for filter options
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        
        # Generate year range for birth years
        context['birth_years'] = range(1920, 2005)
        
        # Pass current filter values back to template
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_min_birth_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_birth_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')
        
        return context


class VoterDetailView(DetailView):
    """Display detailed information for a single voter.
    
    Shows personal information, address with Google Maps link, and
    complete voting history across all tracked elections."""

    model = Voter
    template_name = 'voter_analytics/show_voter.html'
    context_object_name = 'voter'


class VoterListGraphsView(ListView):
    """Display data visualizations (charts and graphs) for voter analytics."""

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'


    def get_queryset(self):
        """Return filtered queryset of voters based on GET parameters.
        
        Applies the same filtering logic as VoterListView to ensure
        visualizations reflect the filtered dataset."""

        queryset = Voter.objects.all()
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        voter_score = self.request.GET.get('voter_score')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')

        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        
        # Apply filters if provided
        if party:
            queryset = queryset.filter(party__icontains=party)

        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        if min_birth_year:
            queryset = queryset.filter(date_birth__year__gte=min_birth_year)

        if max_birth_year:
            queryset = queryset.filter(date_birth__year__lte=max_birth_year)
        
        if v20state:
            queryset = queryset.filter(v20state=(v20state == 'true'))
        
        if v21town:
            queryset = queryset.filter(v21town=(v21town == 'true'))
        
        if v21primary:
            queryset = queryset.filter(v21primary=(v21primary == 'true'))
        
        if v22general:
            queryset = queryset.filter(v22general=(v22general == 'true'))
        
        if v23town:
            queryset = queryset.filter(v23town=(v23town == 'true'))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Generate Plotly visualizations and add to template context.
        
        Creates three interactive charts: pie chart for party distribution,
        bar chart for birth year distribution, and histogram for election
        participation. All charts reflect the currently applied filters.
        """
        context = super().get_context_data(**kwargs)
        context['voter_count'] = self.get_queryset().count()
        
        # Get distinct values for filter options
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        
        # Generate year range for birth years
        context['birth_years'] = range(1919, 2005)
        
        # Pass current filter values back to template
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_min_birth_year'] = self.request.GET.get('min_birth_year', '')
        context['selected_max_birth_year'] = self.request.GET.get('max_birth_year', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')


        filtered_voters = self.get_queryset()

        parties_filtered_count_dicc = {}
        
        year_filtered_count_dicc = {}

        vote_filtered_count_dicc = {
            'v20state': {'voted': 0, 'not_voted': 0},
            'v21town': {'voted': 0, 'not_voted': 0},
            'v21primary': {'voted': 0, 'not_voted': 0},
            'v22general': {'voted': 0, 'not_voted': 0},
            'v23town': {'voted': 0, 'not_voted': 0}
        }
        
        # Parties chart diccionary
        for voter in filtered_voters:
            if voter.party in parties_filtered_count_dicc:
                parties_filtered_count_dicc[voter.party] += 1
            else:
                parties_filtered_count_dicc[voter.party] = 1

        # Year distribution chart diccionary      
        for voter in filtered_voters:
            if voter.date_birth.year in year_filtered_count_dicc:
                year_filtered_count_dicc[voter.date_birth.year] += 1
            else:
                year_filtered_count_dicc[voter.date_birth.year] = 1
        
        # Participation in election chart diccionary  
        for voter in filtered_voters:
            if 'v20state' not in vote_filtered_count_dicc:
                vote_filtered_count_dicc['v20state'] = {'voted': 0, 'not_voted': 0}
            if voter.v20state:
                vote_filtered_count_dicc['v20state']['voted'] += 1
            else:
                vote_filtered_count_dicc['v20state']['not_voted'] += 1
            
            if 'v21town' not in vote_filtered_count_dicc:
                vote_filtered_count_dicc['v21town'] = {'voted': 0, 'not_voted': 0}
            if voter.v21town:
                vote_filtered_count_dicc['v21town']['voted'] += 1
            else:
                vote_filtered_count_dicc['v21town']['not_voted'] += 1
            
            if 'v21primary' not in vote_filtered_count_dicc:
                vote_filtered_count_dicc['v21primary'] = {'voted': 0, 'not_voted': 0}
            if voter.v21primary:
                vote_filtered_count_dicc['v21primary']['voted'] += 1
            else:
                vote_filtered_count_dicc['v21primary']['not_voted'] += 1
            
            if 'v22general' not in vote_filtered_count_dicc:
                vote_filtered_count_dicc['v22general'] = {'voted': 0, 'not_voted': 0}
            if voter.v22general:
                vote_filtered_count_dicc['v22general']['voted'] += 1
            else:
                vote_filtered_count_dicc['v22general']['not_voted'] += 1
            
            if 'v23town' not in vote_filtered_count_dicc:
                vote_filtered_count_dicc['v23town'] = {'voted': 0, 'not_voted': 0}
            if voter.v23town:
                vote_filtered_count_dicc['v23town']['voted'] += 1
            else:
                vote_filtered_count_dicc['v23town']['not_voted'] += 1

        # Bar Chart B(irth Year Distribution)
        x = []
        y = []

        for key in year_filtered_count_dicc.keys():
            x.append(key)
        
        for value in year_filtered_count_dicc.values():
            y.append(value)

        fig = go.Bar(x=x, y=y)
        title_text = "Voter Distribution by Birth Year"
        graph_bar_div_splits = plotly.offline.plot({"data": [fig],
                                                    "layout_title_text": title_text},
                                                    auto_open=False,
                                                    output_type='div')
        
        context['graph_distribution_div_splits'] = graph_bar_div_splits

        # Pie Graph (Affiliated Party)
   
        x = []
        y = []

        for key in parties_filtered_count_dicc.keys():
            x.append(key)
        
        for value in parties_filtered_count_dicc.values():
            y.append(value)

        fig = go.Pie(labels=x, values=y)

        title_text = "Voter Party Distribution"
        graph_pie_div_splits = plotly.offline.plot({"data": [fig], 
                                                "layout_title_text": title_text},
                                                auto_open=False,
                                                output_type='div')
        context['graph_pie_div_splits'] = graph_pie_div_splits

        # Histogram (Election Participation)
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_keys = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        
        voted_counts = [vote_filtered_count_dicc[key]['voted'] for key in election_keys]
        
        fig = go.Bar(x=elections, y=voted_counts)
        title_text = "Voter Participation by Election"
        graph_histogram_div = plotly.offline.plot({"data": [fig],
                                                   "layout_title_text": title_text},
                                                   auto_open=False,
                                                   output_type='div')
        
        context['graph_histogram_div_splits'] = graph_histogram_div

        return context
    
